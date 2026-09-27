# OLAP Database Selection Framework

Choosing an analytical database engine is not a beauty contest or a race to declare a "fastest database in the world." Every analytical engine makes explicit architectural tradeoffs between ingestion throughput, mutation flexibility, query latency, hardware cost, operational complexity, and SQL expressiveness.

---

## 1. The 17 Architectural Selection Questions

Before selecting an analytical engine, evaluate your system against these 17 concrete dimensions:

| Dimension | Key Question | Tradeoff Implication |
| :--- | :--- | :--- |
| **1. Data Scale** | What is the uncompressed data volume (10 GB, 1 TB, 100 TB, 10 PB)? | Sub-100GB fits on single-node DuckDB/PostgreSQL; Multi-TB demands ClickHouse/Druid/Pinot/Cloud DWH. |
| **2. Ingestion Pattern** | Batch (hourly/daily files) or Streaming (Kafka/Kinesis event streams)? | Druid/Pinot natively ingest from Kafka topics; DuckDB prefers Parquet/S3; ClickHouse excels at both buffered batch & Kafka engine. |
| **3. Freshness SLA** | How soon after event generation must data be queryable (seconds vs minutes vs hours)? | Sub-second freshness requires streaming architectures (ClickHouse/Pinot/Druid); batch lakes (Parquet/DuckDB) require compaction cycles. |
| **4. Query Workload Shape** | Fixed parameterized dashboard queries or unpredictable ad-hoc analyst exploration? | Fixed dashboards benefit from pre-aggregation rollups, projections, and star-trees (Druid/Pinot/ClickHouse); ad-hoc queries need full SQL engines (DuckDB/ClickHouse/Trino). |
| **5. Query Latency Target** | Sub-50ms (user-facing embedded analytics) or 500ms–5s (internal BI reporting)? | Sub-50ms requires segment index caches and star-trees (Pinot/Druid/ClickHouse); DuckDB/Presto target interactive 200ms–2s. |
| **6. Query Concurrency** | 5 concurrent data scientists or 10,000 concurrent web users refreshing dashboards? | High concurrency on point-analytical queries favors Pinot/ClickHouse with replica scaling; DuckDB is single-process embedded. |
| **7. Dimension Cardinality** | Low-cardinality categories (country, status) or extreme cardinality (UUIDs, user IDs)? | Extreme cardinality stresses memory and bitmap indexes; ClickHouse handles raw scans well; Druid bitmaps degrade if cardinality exceeds 1M+. |
| **8. Mutations & Updates** | Immutable append-only events, or frequent row updates and GDPR deletes? | Column stores penalize row mutations. PostgreSQL handles ACID updates; ClickHouse uses `ReplacingMergeTree` or asynchronous `ALTER UPDATE`; Druid requires segment rewriting. |
| **9. Join Complexity** | Single denormalized wide table, or complex multi-way snowflake joins? | DuckDB and PostgreSQL excel at arbitrary joins; ClickHouse prefers wide tables or star joins; Druid/Pinot have historically limited join support. |
| **10. SQL Standard Completeness** | Full ANSI SQL (correlated subqueries, recursive CTEs, window functions) or restricted OLAP subset? | DuckDB and PostgreSQL provide near 100% ANSI compliance; ClickHouse provides rich analytical functions; Druid/Pinot support a narrower SQL dialect. |
| **11. Deployment Architecture** | Embedded in-process library or client-server service? | DuckDB runs in-process with zero network overhead (ideal for CLI, microservices, lambda); ClickHouse/Druid/Pinot run as dedicated clusters. |
| **12. Scalability Model** | Single large box (scale-up) or horizontal cluster (scale-out)? | Modern multi-core NVMe servers handle billions of rows on single-node ClickHouse/DuckDB; multi-PB requires distributed Druid/ClickHouse clusters. |
| **13. Storage Decoupling** | Local NVMe disks (shared-nothing) or cloud object store (S3/GCS with shared-storage)? | Local NVMe maximizes raw scan bandwidth; decoupled cloud storage (ClickHouse Cloud, Snowflake, BigQuery) minimizes storage costs. |
| **14. Pre-aggregation Tolerance** | Is approximate/rolled-up data acceptable, or must raw granular events be queryable indefinitely? | Ingestion rollup (Druid) shrinks storage by 90%+ but permanently destroys individual transaction details. |
| **15. Retention & Lifecycle** | Do older partitions age out via TTL or tier to colder object storage? | Built-in TTL policies (ClickHouse `TTL`, Druid retention rules) automate data tiering. |
| **16. Operational Footprint** | Zero-ops embedded binary vs multi-component cluster (ZooKeeper/Etcd, Broker, Router, Coordinator, Historicals)? | DuckDB requires zero administration; ClickHouse is single-binary or Keeper-coordinated; Druid/Pinot require coordinating 4–6 distributed roles. |
| **17. Cloud Economics** | Self-hosted hardware or managed serverless cloud (BigQuery, Snowflake)? | Managed cloud offers elasticity without sysadmin overhead but introduces variable scan-based query costs. |

---

## 2. Comparative Engine Architecture Matrix

| Capability / Trait | DuckDB | ClickHouse | Apache Druid | Apache Pinot | PostgreSQL |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Architecture** | In-process vectorized engine | Standalone / Distributed Columnar DBMS | Distributed time-partitioned event OLAP | Distributed real-time serving OLAP | Single-node relational ACID row store |
| **Storage Layout** | Columnar file / memory blocks | Columnar immutable parts (`MergeTree`) | Columnar immutable segment files | Columnar immutable segment files | Row-oriented 8KB heap pages |
| **Execution Model** | Vectorized push-based chunk pipeline (2048 rows) | Vectorized SIMD-accelerated blocks (65k rows) | Scatter-gather distributed segment scan | Scatter-gather distributed segment scan | Volcano iterator (tuple-at-a-time) |
| **Native Ingestion** | Parquet, CSV, Arrow, Iceberg direct read | Native batch insert, Kafka engine, S3 | Kafka/Kinesis indexing service, batch jobs | Kafka/Kinesis stream ingestion, Spark/offline | Row-by-row `INSERT`, `COPY` |
| **Update / Delete Cost** | Standard table rewrite / delete mask | Asynchronous mutations (`ALTER TABLE UPDATE/DELETE`), `ReplacingMergeTree` | Segment compaction / tombstone rewrite | Table-level upsert tracking with primary key | Fast ACID row-level MVCC updates |
| **Index Types** | Min/max zone maps, ART index | Primary sparse index (granules), Bloom filters, MinMax, TokenBF | Columnar bitmap indexes, spatial, dictionary | Star-tree, inverted index, Bloom filter, range | B-Tree, BRIN, GIN, GiST, Hash |
| **Best-Fit Workload** | Local data science, Parquet lake analytics, embedded apps | High-throughput event logs, product analytics, observability | Real-time dashboards, timeseries metrics with rollup | Low-latency user-facing app analytics, fast slicing | Transactional OLTP, mixed OLTP/OLAP < 50 GB |
| **Major Anti-Pattern** | High-concurrency multi-user server | High-frequency single-row updates/point lookups | Complex ad-hoc multi-table joins | Unindexed deep exploratory queries | Multi-column full scans across 100M+ rows |

---

## 3. Decision Archetypes

### Archetype A: The Local Data Analyst & Data Science Pipeline
- **Workload**: Reading 50 GB of Parquet files on a laptop or container to run aggregations, window functions, and model features.
- **Optimal Choice**: **DuckDB**. Zero network hops, reads Parquet projection pushdown natively, executes in vectorized C++ speed.

### Archetype B: The High-Volume Event Analytics Platform (Clickstream / Observability)
- **Workload**: 100,000+ events per second ingested continuously; analysts query raw events and hourly aggregated rollups over billions of rows.
- **Optimal Choice**: **ClickHouse**. Unmatched compression ratios (LZ4/ZSTD/T64), blazing raw scan speeds via vectorized MergeTree, incremental materialized views for real-time dashboards.

### Archetype C: Real-Time Stream Ingestion with Aggregation Rollup
- **Workload**: Millions of IoT/telemetry metrics streaming from Kafka where individual event details can be summarized into 1-minute aggregates at ingestion time.
- **Optimal Choice**: **Apache Druid**. Ingestion-time rollup, time-chunked segments, native bitmap indexes for slicing across low-cardinality dimensions.

### Archetype D: User-Facing Embedded Analytics API
- **Workload**: 5,000 concurrent mobile app users refreshing their personal profile analytics; SLA requires p95 latency under 30ms.
- **Optimal Choice**: **Apache Pinot** or **ClickHouse**. Pinot's star-tree index and replica routing deliver ultra-low latency serving for structured queries.

### Archetype E: The Moderate Analytics Workload (< 50 GB) on an Existing Application
- **Workload**: E-commerce transactional app needing daily sales reports and monthly revenue aggregates over 5 million orders.
- **Optimal Choice**: **PostgreSQL**. Do NOT add the operational overhead of a distributed columnar database when an existing PostgreSQL instance with proper indexes (or BRIN on `created_at`) can answer the query in 200ms.
