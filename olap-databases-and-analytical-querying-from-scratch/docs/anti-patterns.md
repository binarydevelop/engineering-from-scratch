# OLAP Anti-Patterns: Architectural Diagnoses & Cures

Every anti-pattern documented here represents a real-world engineering failure mode. For each anti-pattern, we dissect:
1. **Why Tempting**: The intuitive developer shortcut.
2. **Physical Problem**: What happens at the CPU, memory, and disk layers.
3. **Symptom**: How it manifests in logs, metrics, and user experience.
4. **Measurement**: The exact metrics and queries that expose the pathology.
5. **Better Option**: The mechanically sound architecture.
6. **When It Might Be Justified**: The narrow edge case where it is acceptable.

---

## 1. OLAP Database for OLTP
- **Why Tempting**: The team sees ClickHouse scanning 100M rows in 20ms and assumes it will make their web application's user CRUD operations fast.
- **Physical Problem**: Columnar engines organize data in large compressed column parts (thousands of rows). Point updates and single-row inserts require rewriting entire compressed column chunks, creating massive write amplification. Lack of row-level locking and transaction serialization breaks ACID guarantees.
- **Symptom**: "Too many parts" exceptions, thread pool exhaustion, queries returning stale unmerged data, extreme disk I/O from background merges.
- **Measurement**: ClickHouse `system.parts` showing thousands of tiny parts; background merge CPU exceeding 80%.
- **Better Option**: Use PostgreSQL or MySQL for operational OLTP, and replicate changes via CDC (Debezium/Kafka) or micro-batches into the OLAP engine.
- **When Justified**: Never. OLAP storage engines are physically antithetical to high-frequency point updates.

---

## 2. PostgreSQL for Unlimited Analytics
- **Why Tempting**: PostgreSQL is already deployed, trusted, ACID-compliant, and well-understood by the team.
- **Physical Problem**: PostgreSQL is a row-oriented heap engine with 8KB pages. To aggregate 2 columns across 500 million rows, PostgreSQL must read every single 8KB page containing all 40 unreferenced columns from disk into `shared_buffers`, saturating memory bandwidth and disk I/O.
- **Symptom**: Buffer cache eviction of operational OLTP working sets, high `iowait`, queries running for minutes, CPU bound in tuple-deserialization loops.
- **Measurement**: `EXPLAIN (ANALYZE, BUFFERS)` showing millions of shared hit/read blocks and 99% I/O time spent discarding irrelevant attributes.
- **Better Option**: For analytics over 10M+ rows, offload analytical queries to DuckDB (for file/Parquet queries) or ClickHouse.
- **When Justified**: When dataset size is under 10–20 GB, fits entirely in RAM, and BRIN indexes on timestamps suffice to satisfy reporting SLAs.

---

## 3. SELECT *
- **Why Tempting**: Convenience during query drafting; developer doesn't want to type 12 column names.
- **Physical Problem**: In columnar storage, each column is stored in an independent file or block. `SELECT *` forces the storage engine to open, decompress, and decode every single column on disk—even if the downstream code only reads 2 columns.
- **Symptom**: 10× to 50× increase in disk I/O, cache thrashing, high query latency, massive cloud scan bills in BigQuery/Snowflake.
- **Measurement**: Profiler showing `BytesRead` matching uncompressed table size instead of a fraction thereof.
- **Better Option**: Explicitly project only the columns strictly required by the downstream consumer: `SELECT timestamp, country, revenue`.
- **When Justified**: Ad-hoc terminal debugging when inspecting 5 sample rows (`LIMIT 5`).

---

## 4. Partition by Everything
- **Why Tempting**: Belief that if partitioning by date is good, then partitioning by `(date, region, category, status)` must be even better.
- **Physical Problem**: Partitioning physically splits tables into distinct directory paths or MergeTree parts. High partition counts lead to millions of tiny files, metadata table bloat, file handle exhaustion, and degraded sequential I/O.
- **Symptom**: File system inode exhaustion, ClickHouse crashes with "Too many parts in all data parts in table", slow startup times.
- **Measurement**: Checking filesystem directory count or ClickHouse `system.parts` count exceeding 5,000 active parts.
- **Better Option**: Partition coarsely (e.g., by month or day). Use sorting keys (`ORDER BY`) inside parts for fine-grained skipping.
- **When Justified**: Never. Partitioning is for data lifecycle management (dropping an entire month with `DROP PARTITION`), not for fine data filtering.

---

## 5. High-Cardinality Partitioning
- **Why Tempting**: Partitioning by `user_id` or `device_uuid` so queries for a single user are fast.
- **Physical Problem**: If you have 5 million users, partitioning by `user_id` creates 5 million directories and 5 million tiny files. Column compression fails completely because each file contains only a handful of values.
- **Symptom**: ClickHouse refactor fail, OS out of file descriptors, total ingestion halt.
- **Measurement**: `SELECT count(DISTINCT partition) FROM system.parts` showing $> 10,000$.
- **Better Option**: Partition by time (`toYYYYMM(event_time)`) and place `user_id` as the leading prefix of the `ORDER BY` sorting key.
- **When Justified**: Multi-tenant B2B architectures where tenant count is bounded (< 100 large enterprise tenants) and isolation requires tenant-level drops.

---

## 6. Wrong Sort Key
- **Why Tempting**: Ordering by `id` or primary key out of habit from relational databases.
- **Physical Problem**: OLAP engines rely on sort keys to build sparse primary indexes and min/max zone maps. If a table is sorted by `id`, but all queries filter by `(tenant_id, event_time)`, the engine cannot prune granules and must perform a full scan of every column.
- **Symptom**: Queries take seconds instead of milliseconds; data skipping index efficiency drops to 0%.
- **Measurement**: ClickHouse `query_log` showing `read_rows` equals total table rows despite selective `WHERE` clauses.
- **Better Option**: Order by the most selective and frequently filtered columns first: `ORDER BY (tenant_id, event_date, event_time)`.
- **When Justified**: When queries exhibit completely random access across 20 dimensions with no dominant filtering pattern (rare; in such cases, consider projections).

---

## 7. Index Everything
- **Why Tempting**: In OLTP, adding B-trees speeds up point lookups, so developers add data skipping indexes or secondary indexes to every column.
- **Physical Problem**: Inverted indexes and data skipping indexes consume memory and CPU during ingestion and slow down merges. In a columnar engine, scanning a compressed column sequentially is often faster than evaluating a secondary index.
- **Symptom**: Slower ingestion throughput, inflated storage footprint, query plans choosing inefficient index probes over fast SIMD vector scans.
- **Measurement**: ClickHouse `system.data_skipping_indices` showing low skipping ratios accompanied by high index disk size.
- **Better Option**: Rely primarily on sorting key ordering. Add secondary skipping indexes (e.g., Bloom filters) only to high-cardinality search strings that cannot be placed in the primary sort key.
- **When Justified**: Specific token searches (e.g. error codes, log message tokens) via Bloom filter (`tokenbf_v1`).

---

## 8. Huge GROUP BY
- **Why Tempting**: Running ad-hoc aggregations grouping by 5 high-cardinality fields (`user_id`, `session_id`, `ip_address`, `url`, `timestamp`).
- **Physical Problem**: The engine must instantiate an in-memory hash table with an entry for every unique combination. Millions of entries cause severe L3 cache misses, pointer chasing, memory bloat, and disk spilling.
- **Symptom**: Memory limit exceeded errors (`Memory limit (for query) exceeded`), severe CPU degradation, query spill to disk slowing latency by 20×.
- **Measurement**: Checking peak memory usage in `system.query_log` or DuckDB memory profiler.
- **Better Option**: Reduce grouping granularity, filter before grouping, or use two-phase distributed aggregation.
- **When Justified**: Bounded batch reconciliation pipelines where high memory limits and external spill are explicitly provisioned.

---

## 9. Exact Everything
- **Why Tempting**: Insisting on `COUNT(DISTINCT user_id)` and exact 99th percentile across 2 billion rows for a high-level executive dashboard.
- **Physical Problem**: Exact distinct counting requires storing every unique 64-bit ID in a hash set or bitmap. Computing exact percentiles requires sorting the entire unaggregated dataset in memory.
- **Symptom**: Dashboard queries take 30+ seconds and consume 16 GB RAM just to tell the user that traffic was roughly 42 million.
- **Measurement**: Comparing memory and latency of `COUNT(DISTINCT x)` vs `approx_count_distinct(x)` / `uniqHLL12(x)`.
- **Better Option**: Use HyperLogLog (`uniq(x)` or `approx_count_distinct`) for distinct counts (typical 1–2% error, 99% less memory) and t-digest / DDSketch for quantiles (`quantileTiming` / `approx_quantile`).
- **When Justified**: Financial auditing, legal compliance, or billing reconciliation where exact precision is legally required.

---

## 10. Preaggregate Everything
- **Why Tempting**: Fear of slow queries leads architects to pre-aggregate all metrics at ingestion time into rigid daily cubes.
- **Physical Problem**: Pre-aggregation destroys the grain of the data. Once aggregated into `(day, country, total_revenue)`, you can never ask for hourly patterns, user-level cohorts, or ad-hoc dimension cross-filtering.
- **Symptom**: Product team constantly requests new pipeline changes because the pre-aggregated table cannot answer new analytical questions.
- **Measurement**: High data engineering backlog maintaining dozens of custom summary tables.
- **Better Option**: Store raw event facts in an optimized columnar format. Raw scans on modern engines are fast enough for most ad-hoc needs; pre-aggregate only proven high-frequency dashboard queries.
- **When Justified**: Telemetry/IoT systems ingesting billions of events per second where retention of raw sensor readings beyond 7 days is economically impossible.

---

## 11. Materialized View Cargo Cult
- **Why Tempting**: Creating a materialized view for every chart on every internal dashboard.
- **Physical Problem**: Every insert triggers downstream transformation into every materialized view. Write amplification explodes, background ingestion stalls, and disk usage multiplies.
- **Symptom**: Ingestion lag builds up, system memory is consumed maintaining intermediate aggregate states, disk fills up rapidly.
- **Measurement**: Measuring CPU and disk write amplification on the database server during batch ingestion.
- **Better Option**: Consolidate multiple dashboard metrics into a single unified summary table with mergeable aggregate states (`AggregateFunction`).
- **When Justified**: High-traffic production APIs serving public dashboards with strict SLA (< 100ms) under high concurrency.

---

## 12. Tiny Inserts
- **Why Tempting**: Treating the OLAP database like a web service backend: inserting 1 row whenever an API endpoint is hit.
- **Physical Problem**: Each insert creates a distinct, uncompressed physical part or file. The database engine is forced into a continuous frenzy of background merges to prevent part explosion.
- **Symptom**: Error: `Too many parts in all data parts in table (300). Merges are processing significantly slower than inserts.`
- **Measurement**: Monitoring insert rate vs active parts count in `system.parts`.
- **Better Option**: Buffer writes in application memory, Redis, or Kafka, and flush in batches of 10,000 to 100,000 rows (or at least once every 1–5 seconds). In ClickHouse, enable asynchronous inserts (`SET async_insert = 1, wait_for_async_insert = 0`).
- **When Justified**: Never in direct synchronous client writes.

---

## 13. Tiny Files (The Small Files Problem in Data Lakes)
- **Why Tempting**: Streaming jobs (e.g. Flink or Spark) writing 100KB Parquet files to S3 every 10 seconds.
- **Physical Problem**: Opening and closing thousands of HTTP object store connections introduces severe network latency. File footer metadata parsing dominates query execution time instead of actual vector scanning.
- **Symptom**: DuckDB or Spark spending 90% of query time reading metadata and 10% scanning data.
- **Measurement**: Listing file count and average file size: 10,000 files averaging 250 KB is a disaster.
- **Better Option**: Run background compaction jobs to merge files into optimal chunks of 128 MB to 512 MB.
- **When Justified**: Temporary staging landings before automated compactor consolidation.

---

## 14. Mutation-Heavy OLAP
- **Why Tempting**: Attempting to implement an e-commerce order status workflow (Pending -> Paid -> Shipped -> Delivered) directly in a columnar table with `UPDATE orders SET status = ... WHERE id = ...`.
- **Physical Problem**: Columnar storage formats are immutable. An update requires either rewriting entire column chunks or maintaining expensive delete masks and row-delta files that must be reconciled during every scan.
- **Symptom**: High merge backlog, massive CPU consumption during idle periods, erratic query latency.
- **Measurement**: Checking background merge tasks and disk write I/O after running batch updates.
- **Better Option**: Model mutable status as an append-only event log (`order_status_events`) and compute the current status at query time or using `ReplacingMergeTree` / `argMax(status, updated_at)`.
- **When Justified**: Infrequent bulk compliance operations (e.g. GDPR "Right to be Forgotten" monthly scrubs).

---

## 15. Benchmark Theater
- **Why Tempting**: Running a single hand-picked query three times in a row on a primed warm cache, taking a screenshot of the 4ms execution time, and publishing a blog post declaring "Database X is 100x faster than Database Y."
- **Physical Problem**: Warm-cache runs test RAM and OS page-cache speed, not the engine's disk I/O, compression codecs, or data skipping mechanisms. Hand-picked queries exploit engine-specific shortcuts while ignoring real-world concurrency, ingestion, and memory pressure.
- **Symptom**: Production deployment fails to deliver the promised benchmark speed; system crashes under concurrent load or out-of-order data.
- **Measurement**: Always benchmark cold cache vs warm cache, test under concurrent workloads (16–64 queries), and log exact hardware, rows scanned, and bytes read.
- **Better Option**: Follow `BENCHMARK_TEMPLATE.md` with transparent hardware, data distribution, and limitation logging.
- **When Justified**: Never. Dishonest benchmarking damages architectural credibility.

---

## 16. Real-Time Everything
- **Why Tempting**: Building a complex Kafka + Flink + Pinot streaming architecture with 2-second SLA because "real-time sounds modern and agile."
- **Physical Problem**: Real-time streaming infrastructure requires ZooKeeper/Kafka brokers, schema registries, stream processing nodes, out-of-order event handling, and 24/7 on-call operational overhead.
- **Symptom**: The business team only looks at the dashboard once on Monday morning at 9:00 AM, while engineers spend nights debugging consumer lag and partition rebalances.
- **Measurement**: Checking query access logs: if dashboard refresh frequency is hourly or daily, real-time streaming is pure waste.
- **Better Option**: Simple batch ingestion (hourly or daily Parquet export to DuckDB or ClickHouse) costs 90% less and is 10× easier to operate.
- **When Justified**: Automated algorithmic trading, fraud detection, security anomaly alerting, or live user-facing delivery tracking where decisions are made within seconds of event occurrence.

---

## 17. ClickHouse / Druid Because "Big Data"
- **Why Tempting**: Resume-driven development: deploying a 3-node distributed ClickHouse or Druid cluster for a startup with 5 GB of total historical data.
- **Physical Problem**: Running distributed analytical databases for small datasets introduces network latency, cluster consensus overhead, and unnecessary hardware cost.
- **Symptom**: High AWS bill for idle EC2 instances; hours spent upgrading cluster versions instead of writing product features.
- **Measurement**: `SELECT pg_size_pretty(pg_database_size('app_db'))` or total Parquet size $< 20\text{ GB}$.
- **Better Option**: Run DuckDB directly against Parquet files or run PostgreSQL with proper indexing. A single 16-core laptop with DuckDB can scan 5 GB of Parquet in under 50 milliseconds.
- **When Justified**: When data volume is growing exponentially ($> 100\text{ GB}$ per month) with a clear roadmap requiring scale-out within 6 months.
