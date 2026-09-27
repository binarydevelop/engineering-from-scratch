# Curriculum Roadmap: Data Engineering From Scratch

> **Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.**

An exhaustive, 20-part curriculum spanning **201 phases (Phase 00 through Phase 200)**.
Every phase forces the learner to begin from first principles, evaluate data and system failures, and derive architectural primitives under operational constraints.

---

## Curriculum Structure at a Glance

| Part | Title | Phase Range | Core Architectural Theme |
| :--- | :--- | :--- | :--- |
| **01** | Foundations, Records & File Formats | 00–10 | Data Engineering Lab, records, CSV RFC 4180, nested JSON, schemas, validation gates, row vs columnar, Parquet, compression, batch primitives |
| **02** | Ingestion & Relational Operational Sources | 11–20 | ETL vs ELT, file ingestion, API pagination & rate limits, incremental watermarks, idempotency, checkpoints, backfills, lineage intuition, OLTP vs OLAP |
| **03** | Warehousing & Dimensional Modeling | 21–32 | Why warehouses exist, warehouse mental model, facts & dimensions, grain definition, star schemas, SCD Type 1 & 2, surrogate keys, SQL CTEs, staging, intermediate, marts, SQL testing |
| **04** | Analytics Engineering & Orchestration | 33–45 | dbt introduction, models & compilation, generic/custom tests, sources & freshness, snapshots, DAG dependency graphs, Python orchestrator from scratch, retries, scheduling, Airflow DAGs & backfills |
| **05** | Partitioning, Lakes & Open Table Formats | 46–58 | Partitioned storage, partition pruning, partition keys & skew, small files problem, compaction, object storage mental model (S3/MinIO), data lakes, zones, schema-on-read vs write, Iceberg table formats, snapshots & time travel, schema evolution |
| **06** | Distributed Compute & Apache Spark | 59–70 | The distributed compute problem, Map/Reduce from first principles, compute partitioning, network shuffle, Spark architecture, DataFrames & Catalyst, lazy evaluation, narrow vs wide transformations, broadcast joins, data skew salting, memory spill, tuning loop |
| **07** | Change Data Capture (CDC) | 71–76 | CDC motivation, CDC from first principles, WAL & transaction logs, Debezium tooling, baseline snapshot + CDC stream merge, consumer failure recovery & LSN checkpoints |
| **08** | Streaming Systems & Event Time | 77–91 | The streaming problem, event logs & offsets, event time vs processing time, late-arriving data, tumbling & sliding & session windows, watermarks, state stores, exactly-once reality, stream engines, checkpoints, replay, batch vs streaming comparison, Lambda & Kappa |
| **09** | Data Quality, Contracts & Schemas | 92–100 | Quality from first principles, the 6 quality dimensions, automated test gates, statistical distribution anomalies, freshness SLAs, volume anomalies, data contracts, schema compatibility modes, CI contract testing |
| **10** | Metadata, Catalogs & Lineage | 101–105 | Metadata fundamentals, data catalog concept, automated SQL AST lineage, ownership & operational accountability, the 5 pillars of data observability |
| **11** | Reliability, Atomic Commits & Security | 106–119 | Structured logging, Prometheus metrics, SLAs & SLOs, recovery protocols, staging & atomic commits, partition replacement, poison records, dead-letter queues (DLQ), raw replayability, retention, PII, RBAC & column masking, tokenization, practical governance |
| **12** | Warehouse Performance & Data Modeling | 120–130 | Query plan analysis, partitioning vs clustering/Z-order, query cost engineering, materialized rollups, incremental models, event deduplication, surrogate event IDs, late-arriving dimensions, referential integrity, cross-system reconciliation, financial ledger balance |
| **13** | CI/CD, Deployment & Safe Migrations | 131–137 | Pipeline versioning, deterministic reproducibility, dev/staging/prod environments, CI test automation, deployment vs backfills, blue/green model migrations, dataset diffing |
| **14** | Source Protection, Queues & Scaling | 138–148 | Source extraction impact, read replicas, API rate limit token buckets, backpressure flow control, queue lag planning, batch scaling bottlenecks, streaming consumer rebalancing, hot partitions, cluster sizing tradeoffs, platform cost engineering, data locality |
| **15** | Data Platform Architecture | 149–163 | Platform architecture framework, batch-first platforms, adding orchestration, adding CDC, adding streaming, batch + streaming coexistence, medallion architecture critique, data mesh, data products, storage comparison, OLTP vs warehouse boundaries, stream vs queue, DE vs Backend / Analytics / ML Engineering |
| **16** | End-to-End Applied Projects | 164–180 | E-commerce batch, clickstream funnel, CDC replication, data lake, lakehouse format, dimensional warehouse, dbt project, Airflow DAG, streaming aggregator, data quality engine, lineage tracker, backfill engine, compactor, reconciliation, deduplication, SCD2, catalog CLI |
| **17** | Production Debugging Labs | 181–190 | Duplicate rows & metric doubling, missing historical partition, schema drift crash, late-arriving data drift, stale dashboard green job, small files query degradation, distributed task skew straggler, CDC offset loss, partial publish dirty reads, unconstrained backfill truncation |
| **18** | Comprehensive Broken Pipeline Labs | 191 | 32 realistic broken-pipeline incident scenarios across ingestion, schema, quality, orchestration, streaming, Spark, and storage |
| **19** | Capstone Platforms | 192–197 | Capstone 1: Production Batch Platform; Capstone 2: Real-Time Event Platform; Capstone 3: CDC + Warehouse; Capstone 4: Lakehouse Platform; Capstone 5: Data Observability Platform; Capstone 6: Enterprise Analytics Platform |
| **20** | Failure Day & Enterprise System Design | 198–200 | Failure Day chaos engineering, data platform capacity planning, Phase 200 Final Design Challenge: Global E-Commerce Data Platform |

---

## Detailed Phase Syllabus (Phases 00 to 200)

### Part 01: Foundations, Records & File Formats (Phases 00 - 10)
- **Phase 00: Data Engineering Laboratory** — Local multi-tier environment setup: Python 3.11+, DuckDB, PostgreSQL, sample datasets, environment checker.
- **Phase 01: What Is Data Engineering?** — Operational applications vs data engineering vs analytics engineering vs data science.
- **Phase 02: Data as Records** — Rows, records, fields, types, and serialization formats.
- **Phase 03: CSV From First Principles** — RFC 4180 parsing, delimiters, quoting, embedded commas, and malformed rows.
- **Phase 04: JSON and Semi-Structured Data** — Nested objects, variable arrays, missing keys, and relational flattening.
- **Phase 05: Schema From First Principles** — Why schemas protect meaning; schemaless ambiguity vs explicit contracts.
- **Phase 06: Schema Validation & Gatekeeping** — Ingestion boundary validators: syntactic validity vs semantic validity.
- **Phase 07: Row-Oriented vs Columnar Storage** — Row-wise scanning vs columnar storage physics in aggregations.
- **Phase 08: Apache Parquet Under the Hood** — Parquet metadata, footers, dictionary encoding, and column pruning.
- **Phase 09: Compression Algorithms: Snappy vs GZIP vs ZSTD** — Compression ratios, CPU costs, and scan throughput.
- **Phase 10: Batch Processing From First Principles** — Building a deterministic batch worker in pure Python.

### Part 02: Ingestion & Relational Operational Sources (Phases 11 - 20)
- **Phase 11: ETL vs ELT Tradeoffs** — Extract-Transform-Load vs Extract-Load-Transform in the modern warehouse era.
- **Phase 12: Ingestion From Files** — File ingestion pipelines, corrupted record quarantine, and audit logging.
- **Phase 13: Ingestion From REST APIs** — Paginated REST endpoints, rate limiting, exponential backoff, and cursor checkpoints.
- **Phase 14: Incremental Ingestion Strategies** — Replacing full scans with high-watermark queries (`WHERE updated_at > checkpoint`).
- **Phase 15: Idempotent Pipeline Design** — Eliminating duplicate records: proving $f(f(x)) = f(x)$ on repeated runs.
- **Phase 16: Checkpointing & State Persistence** — Persisting offsets so crashes resume without gaps or duplicates.
- **Phase 17: Historical Backfill Mechanics** — Reprocessing historical intervals safely without corrupting production.
- **Phase 18: Data Lineage Intuition** — Tracing metric provenance from dashboards to raw source files.
- **Phase 19: Relational Source Systems (OLTP)** — Extracting from normalized transaction schemas without impacting app performance.
- **Phase 20: OLTP vs OLAP Architecture** — Point lookups vs high-volume columnar scans and disk page access patterns.

### Part 03: Warehousing & Dimensional Modeling (Phases 21 - 32)
- **Phase 21: Why Analytical Warehouses Exist** — Contention, lock escalation, and query timeouts on transactional DBs.
- **Phase 22: The Warehouse Mental Model** — Sources -> ingestion -> staging -> dimensional models -> data marts.
- **Phase 23: Facts and Dimensions (Kimball Modeling)** — Numeric events (facts) vs contextual descriptive attributes (dimensions).
- **Phase 24: Defining the Grain** — What does exactly one row represent? Preventing metric inflation.
- **Phase 25: The Star Schema** — Building conformed dimensions, fact tables, and multi-dimensional rollup queries.
- **Phase 26: Slowly Changing Dimensions (SCD Type 1 & 2)** — Historical attribute mutations, effective date ranges, and version flags.
- **Phase 27: Surrogate Keys vs Natural Keys** — Decoupling warehouse identity from mutable operational primary keys.
- **Phase 28: SQL Transformations** — Modular analytical transformations using CTEs and window functions.
- **Phase 29: Staging Models** — Normalizing source naming, casting types, and filtering soft deletes.
- **Phase 30: Intermediate Models** — Encapsulating repeated business logic and complex multi-table joins.
- **Phase 31: Data Marts** — Materializing consumer-oriented tables for Sales, Marketing, and Finance.
- **Phase 32: Transformation Testing & Assertions** — Enforcing uniqueness, non-null, and referential constraints in SQL.

### Part 04: Analytics Engineering & Orchestration (Phases 33 - 45)
- **Phase 33: dbt From First Principles** — Resolving SQL script chaos: modular models, `ref()`, and automated docs.
- **Phase 34: dbt Models and DAG Compilation** — Compiling modular transformation graphs to warehouse SQL.
- **Phase 35: dbt Generic and Custom Tests** — Schema assertions (`unique`, `not_null`, `relationships`) and custom tests.
- **Phase 36: Sources and Freshness Monitoring** — Detecting upstream ingestion pipeline stalls and alerting on SLAs.
- **Phase 37: Snapshots and Change Tracking** — Capturing mutable source table history using dbt snapshots.
- **Phase 38: The Pipeline Dependency Graph (DAG)** — Modeling task dependencies and topological sorting.
- **Phase 39: Orchestration From First Principles** — Building a custom topological DAG runner in Python.
- **Phase 40: Retries, State Transitions & Failure** — Task states (`PENDING`, `RUNNING`, `SUCCESS`, `FAILED`, `SKIPPED`) and retry backoff.
- **Phase 41: Scheduling vs Dependency Management** — Cron triggers vs topological execution graphs.
- **Phase 42: Introduce Apache Airflow** — Mapping custom orchestrator concepts to Airflow operators and tasks.
- **Phase 43: Authoring Airflow DAGs** — Building production workflows with TaskFlow API and dependencies.
- **Phase 44: Airflow Retries and Failure Handling** — Handling timeouts, exponential retry backoff, and failure alerts.
- **Phase 45: Backfills in Airflow** — Running historical interval backfills with `logical_date` and `data_interval`.

### Part 05: Partitioning, Lakes & Open Table Formats (Phases 46 - 58)
- **Phase 46: Partitioned Data Architecture** — Physical directory partitioning (`date=YYYY-MM-DD`) to avoid full scans.
- **Phase 47: Partition Pruning in Query Engines** — Skipping unneeded files during analytical query execution.
- **Phase 48: Partition Key Design: Cardinality and Skew** — Avoiding high-cardinality file explosions and partition skew.
- **Phase 49: The Small Files Problem** — Measuring metadata overhead and query slowdown from tiny files.
- **Phase 50: File Compaction Strategies** — Merging fragmented small files into optimal 128 MB–512 MB Parquet chunks.
- **Phase 51: Object Storage Mental Model (S3/MinIO)** — Key prefixes, flat namespaces, and non-POSIX write semantics.
- **Phase 52: Data Lake Architecture** — Scalable object storage + open Parquet file formats.
- **Phase 53: Data Lake Zones: Raw, Clean, Curated** — Organizing storage boundaries into raw landing, conformed, and curated marts.
- **Phase 54: Schema-on-Read vs Schema-on-Write** — Evaluating validation at ingestion vs validation at query time.
- **Phase 55: Why Data Lakes Need Table Formats** — Overcoming ACID limitations, concurrent write conflicts, and blind file scans.
- **Phase 56: Lakehouse Table Formats (Apache Iceberg)** — Snapshot metadata trees, manifest lists, and data file pointers.
- **Phase 57: Snapshots and Time Travel** — Querying older historical snapshots using metadata commit pointers.
- **Phase 58: Schema Evolution in Table Formats** — Adding, dropping, and renaming columns without rewriting data files.

### Part 06: Distributed Compute & Apache Spark (Phases 59 - 70)
- **Phase 59: The Distributed Processing Problem** — Hardware limits when single-node memory and CPU saturate on 500 GB+ datasets.
- **Phase 60: Map / Reduce From First Principles** — Building Map -> Shuffle -> Reduce from scratch in Python.
- **Phase 61: Data Partitioning for Compute** — Balancing dataset partitions across parallel worker processes.
- **Phase 62: The Shuffle: Network Data Movement** — Why `GROUP BY` and `JOIN` require expensive network shuffles.
- **Phase 63: Apache Spark Architecture** — Driver, Cluster Manager, Executors, Tasks, and DataFrame memory models.
- **Phase 64: Spark Structured DataFrames** — Transforming distributed datasets and inspecting Catalyst query plans.
- **Phase 65: Lazy Evaluation and Execution DAGs** — Distinguishing lazy transformations from eager actions.
- **Phase 66: Narrow vs Wide Transformations** — Pipeline-parallel narrow operations vs shuffle-heavy wide operations.
- **Phase 67: Distributed Joins: Sort-Merge vs Broadcast** — Eliminating fact-table shuffles using broadcast hash joins.
- **Phase 68: Data Skew and Stragglers** — Diagnosing hot keys and mitigating compute skew using key salting.
- **Phase 69: Memory Management and Disk Spill** — Executor memory exhaustion, garbage collection, and disk spill.
- **Phase 70: Systematic Spark Performance Tuning** — The empirical tuning loop: plans, partitions, shuffle, skew, verification.

### Part 07: Change Data Capture (CDC) (Phases 71 - 76)
- **Phase 71: Change Data Capture Motivation** — Why nightly batch dumps fail on high-write operational databases.
- **Phase 72: CDC From First Principles** — Building a change stream consumer applying INSERT, UPDATE, DELETE sequentially.
- **Phase 73: Database Transaction Logs (WAL / Binlog)** — Write-Ahead Logs, transaction boundaries, and logical decoding.
- **Phase 74: CDC Tooling (Debezium)** — Capturing PostgreSQL mutations and streaming change events to Kafka.
- **Phase 75: Initial Snapshot + Incremental CDC Stream** — Merging baseline database snapshots with continuous change streams.
- **Phase 76: CDC Failure Recovery and Resumption** — Resuming replication from exact WAL LSN offsets after worker crashes.

### Part 08: Streaming Systems & Event Time (Phases 77 - 91)
- **Phase 77: The Streaming Problem** — Business latency requirements vs architectural and operational complexity.
- **Phase 78: Events, Offsets, and Append-Only Logs** — Partitioned append-only event logs, offsets, and consumer groups.
- **Phase 79: Event Time vs Processing Time** — Action occurrence time on device vs server processing clock.
- **Phase 80: Late-Arriving Data and Windows** — Managing out-of-order records caused by network latency and retries.
- **Phase 81: Streaming Windows: Tumbling, Sliding, Session** — Implementing fixed, sliding, and session event windows.
- **Phase 82: Watermarks and Window Finalization** — Estimating event-time progression and closing late windows safely.
- **Phase 83: Stateful Stream Aggregation** — Calculating rolling metrics (events/min, revenue/5min) with state stores.
- **Phase 84: Stream State Stores and RocksDB** — Managing persistent, fault-tolerant state for stateful stream operators.
- **Phase 85: Exactly-Once Processing Reality** — Deconstructing transactional producers, two-phase commits, and idempotency.
- **Phase 86: Stream Processing Engines** — Introducing dedicated engines (Spark Structured Streaming, Flink, Kafka Streams).
- **Phase 87: Streaming Checkpoints and State Recovery** — Restoring stateful streaming topologies after worker crashes.
- **Phase 88: Stream Reprocessing and Replay** — Rewinding offsets to recompute historical metrics after code updates.
- **Phase 89: Batch vs Streaming: The Definitive Comparison** — Same metric in batch vs streaming: cost, complexity, latency.
- **Phase 90: Lambda Architecture: Historical Context** — Dual batch and speed layers: why synchronization doomed them.
- **Phase 91: Kappa Architecture: Stream-First Processing** — Stream-first architectures where historical replay reads older offsets.

### Part 09: Data Quality, Contracts & Schemas (Phases 92 - 100)
- **Phase 92: Data Quality From First Principles** — Separating job execution success from mathematical correctness.
- **Phase 93: The Six Dimensions of Data Quality** — Completeness, Uniqueness, Validity, Consistency, Freshness, Accuracy.
- **Phase 94: Automated Quality Checks** — Programmatic gates: null checks, unique constraints, range checks, foreign keys.
- **Phase 95: Statistical Distribution Anomaly Detection** — Catching 100x metric spikes when schemas pass validation.
- **Phase 96: Freshness Monitoring and Lag Alerting** — Catching stale data when producers stop updating silently.
- **Phase 97: Volume Anomaly Detection** — Flagging unexpected row count drops or surges before publication.
- **Phase 98: Data Contracts in Practice** — Versioned producer-consumer agreements: schemas, semantics, and SLAs.
- **Phase 99: Schema Evolution Compatibility Modes** — Backward, Forward, Full, and Breaking compatibility rules.
- **Phase 100: Contract Testing in CI/CD** — Blocking breaking schema changes before production release.

### Part 10: Metadata, Catalogs & Lineage (Phases 101 - 105)
- **Phase 101: Metadata Fundamentals** — Technical, operational, and business metadata for data governance.
- **Phase 102: The Data Catalog Concept** — Centralized discovery for dataset schemas, owners, and freshness status.
- **Phase 103: Automated SQL AST Lineage** — Parsing SQL queries to construct end-to-end dependency graphs.
- **Phase 104: Data Ownership and Operational Responsibility** — Assigning code and dataset owners to eliminate orphan pipelines.
- **Phase 105: Data Observability Architecture** — The five pillars: Freshness, Volume, Schema, Quality, and Lineage.

### Part 11: Reliability, Atomic Commits & Security (Phases 106 - 119)
- **Phase 106: Structured Logging for Pipelines** — Emitting structured JSON logs: run IDs, partitions, counts, durations.
- **Phase 107: Pipeline Metrics and Prometheus Telemetry** — Exposing rows/sec, bytes processed, and lag metrics.
- **Phase 108: Service Level Agreements (SLAs & SLOs)** — Data delivery promises and error budget management.
- **Phase 109: Failure Recovery Strategies** — Recovery protocols for partial writes and infrastructure crashes.
- **Phase 110: Staging and Atomic Publication** — Writing to temporary locations and publishing atomically.
- **Phase 111: Atomic Partition Replacement** — Swapping historical partitions in metadata without locking readers.
- **Phase 112: Poison Records and Error Handling** — Preventing a single bad byte from crashing an 8-hour batch run.
- **Phase 113: Quarantine and Dead-Letter Queues (DLQ)** — Routing unprocessable records with error logs for inspection.
- **Phase 114: Replayability From Immutable Sources** — Rebuilding downstream models deterministically from raw logs.
- **Phase 115: Data Retention and Lifecycle Management** — Hot/cold/archive storage tiering and compliance purging.
- **Phase 116: Privacy and Sensitive Data Handling** — Identifying and isolating Personally Identifiable Information (PII).
- **Phase 117: Data Access Control (RBAC & Column Masking)** — Enforcing least-privilege security across analytical tables.
- **Phase 118: Data Masking and Tokenization** — Hashing and tokenizing identifiers while preserving analytical utility.
- **Phase 119: Practical Data Governance** — Pragmatic governance balancing security, ownership, discovery, and speed.

### Part 12: Warehouse Performance & Data Modeling (Phases 120 - 130)
- **Phase 120: Warehouse Performance Analysis** — Profiling scans, hash joins, sorting, and aggregate memory in query plans.
- **Phase 121: Partitioning vs Clustering and Sorting** — Coarse partition pruning vs fine-grained clustering and Z-ordering.
- **Phase 122: Query Cost Engineering** — Modeling financial cost based on scanned bytes and compute hours.
- **Phase 123: Materialized Aggregates and Rollups** — Precomputing expensive daily/monthly rollups for fast dashboards.
- **Phase 124: Incremental Warehouse Models** — Transforming only modified records using merge keys.
- **Phase 125: Event Deduplication Techniques** — Deduplicating high-volume event streams using window functions and caches.
- **Phase 126: Surrogate Event IDs and Collision Risks** — Generating composite surrogate keys when source events lack unique IDs.
- **Phase 127: Late-Arriving Dimensions** — Resolving transactions that arrive before dimension records using placeholder keys.
- **Phase 128: Referential Integrity in Analytical Stores** — Automated testing of foreign keys in lakehouse architectures.
- **Phase 129: Data Reconciliation Systems** — Reconciling record counts, checksums, and financial balances cross-system.
- **Phase 130: Financial-Grade Data Reconciliation** — Cent-accurate reconciliation between gateways, ledgers, and reporting marts.

### Part 13: CI/CD, Deployment & Safe Migrations (Phases 131 - 137)
- **Phase 131: Pipeline and Transformation Versioning** — Tracking code versions and schema migration metadata across runs.
- **Phase 132: Reproducibility in Data Pipelines** — Guaranteeing deterministic outputs given identical code, config, and partitions.
- **Phase 133: Data Environments: Dev, Staging, Prod** — Isolating developer testing environments from production datasets.
- **Phase 134: CI/CD for Data Pipelines** — Automating SQL linting, unit tests, and schema checks in pull requests.
- **Phase 135: Deploying Pipelines: Code vs Data Migration** — Disentangling code deployment from historical data backfills.
- **Phase 136: Blue/Green Data Model Migration** — Deploying table versions side-by-side and switching views with zero downtime.
- **Phase 137: Data Diffing Before Deployment** — Comparing old and new models row-by-row before promoting changes.

### Part 14: Source Protection, Queues & Scaling (Phases 138 - 148)
- **Phase 138: Source System Extraction Impact** — Measuring database contention, replication lag, and locks from ETL scans.
- **Phase 139: Extracting From Read Replicas** — Offloading analytical extraction to replicas while managing replication lag.
- **Phase 140: Managing API Rate Limits and Quotas** — Token-bucket rate limiters and cursor checkpoints for API ingestion.
- **Phase 141: Backpressure in Data Pipelines** — Handling consumer saturation using flow control and buffer signals.
- **Phase 142: Queueing Capacity and Consumer Lag Planning** — Calculating lag growth rates and broker retention buffers.
- **Phase 143: Scaling Batch Processing Jobs** — Scaling batch workers and analyzing coordination/shuffle bottlenecks.
- **Phase 144: Scaling Streaming Jobs** — Scaling streaming consumers by rebalancing partitions and state stores.
- **Phase 145: Hot Partitions and Skew Mitigation** — Balancing skewed traffic across streaming partitions.
- **Phase 146: Small vs Large Cluster Tradeoffs** — Sizing compute clusters: startup overhead vs worker efficiency.
- **Phase 147: Data Platform Cost Engineering** — Modeling total cost of ownership across storage, compute, and network egress.
- **Phase 148: Data Locality and Network Transfer** — Colocating compute with storage to reduce cross-region egress fees.

### Part 15: Data Platform Architecture (Phases 149 - 163)
- **Phase 149: Data Platform Architecture Framework** — Sources, ingestion, storage, warehouse, orchestration, quality, BI.
- **Phase 150: Designing a Batch-First Platform** — Lean analytics platform using Postgres, Parquet, DuckDB, and dbt.
- **Phase 151: Adding Orchestration to the Platform** — Managing workflow dependencies, retries, and scheduled pipelines.
- **Phase 152: Adding Change Data Capture to the Platform** — Integrating continuous CDC streams for near-real-time warehouse updates.
- **Phase 153: Adding Streaming Where Justified** — Targeted stream processing for sub-minute latency products.
- **Phase 154: Batch and Streaming Coexistence** — Operating batch and streaming harmoniously without duplicate logic.
- **Phase 155: Medallion Architecture in Perspective** — Bronze/Silver/Gold as organizational guidelines rather than rigid dogma.
- **Phase 156: The Data Mesh Architectural Pattern** — Decentralized domain ownership, federated governance, and associated costs.
- **Phase 157: Treating Datasets as Data Products** — Packaging datasets with contracts, SLOs, docs, tests, and owners.
- **Phase 158: Warehouse vs Lake vs Lakehouse Decision Matrix** — Selecting storage engines based on query speed, ACID, and cost.
- **Phase 159: Warehouse vs Operational Database Boundaries** — Why analytical warehouses must never serve application transactions.
- **Phase 160: Stream vs Work Queue** — Durable append-only event logs (Kafka) vs transient task queues (RabbitMQ).
- **Phase 161: Data Engineering vs Backend Engineering** — Collaboration protocols between software engineers and data teams.
- **Phase 162: Data Engineering vs Analytics Engineering** — Infrastructure and platform engineering vs warehouse modeling.
- **Phase 163: Data Engineering vs ML Engineering** — Feature stores and training datasets for machine learning systems.

### Part 16: End-to-End Applied Projects (Phases 164 - 180)
- **Phase 164: Project: E-Commerce Batch Pipeline** — End-to-end relational extract -> staging -> star schema -> sales mart.
- **Phase 165: Project: Clickstream Funnel Pipeline** — User clickstream ingestion -> sessions -> conversion funnel metrics.
- **Phase 166: Project: CDC Replication Pipeline** — PostgreSQL WAL stream -> replica table with failure injection.
- **Phase 167: Project: Partitioned Data Lake** — Multi-zone object storage lake with date partitioning and Parquet files.
- **Phase 168: Project: Lakehouse Table Format** — Snapshot commits, time travel, and schema evolution in a lakehouse table.
- **Phase 169: Project: Data Warehouse Star Schema** — Conformed dimensions, fact tables, and executive rollup marts.
- **Phase 170: Project: dbt Analytics Project** — Staging, intermediate, and mart models with schema tests and documentation.
- **Phase 171: Project: Airflow Orchestrated Pipeline** — Orchestrating extract, validate, load, transform, and test in Airflow.
- **Phase 172: Project: Streaming Tumbling Window Engine** — Aggregating event streams into 5-minute tumbling windows.
- **Phase 173: Project: Data Quality Assertion Framework** — Extensible framework for schema, range, and foreign key assertions.
- **Phase 174: Project: SQL AST Lineage Tracker** — Parsing SQL queries to generate upstream/downstream dependency graphs.
- **Phase 175: Project: Partition Backfill Engine** — Reprocessing historical date partitions safely without downtime.
- **Phase 176: Project: Small Files Compactor** — Detecting tiny Parquet files and merging them into optimal chunks.
- **Phase 177: Project: Cross-System Financial Reconciliation** — Reconciling payment gateway events against warehouse ledgers.
- **Phase 178: Project: Exact-Once Event Deduplication** — Deduplicating event streams using Bloom filters and window caches.
- **Phase 179: Project: SCD Type 2 Dimension Engine** — Maintaining customer attribute audit trails with effective date ranges.
- **Phase 180: Project: Data Catalog Lite CLI** — Searchable CLI for inspecting dataset schemas, owners, and freshness.

### Part 17: Production Debugging Labs (Phases 181 - 190)
- **Phase 181: Debugging Lab: Duplicate Rows & Metric Doubling** — Diagnosing doubled revenue caused by non-unique joins.
- **Phase 182: Debugging Lab: Missing Historical Partition** — Investigating missing daily partitions in orchestrated workflows.
- **Phase 183: Debugging Lab: Upstream Schema Drift** — Resolving pipeline crashes caused by upstream column type changes.
- **Phase 184: Debugging Lab: Late-Arriving Event Metric Drift** — Diagnosing why historical metrics shifted after late mobile events arrived.
- **Phase 185: Debugging Lab: Stale Dashboard Despite Green Job** — Investigating green job execution where source data stopped updating.
- **Phase 186: Debugging Lab: Small Files Query Degradation** — Remediating 10-minute query scan times caused by 50,000 tiny files.
- **Phase 187: Debugging Lab: Distributed Task Straggler & Skew** — Resolving task duration bottlenecks caused by hot partition keys.
- **Phase 188: Debugging Lab: CDC Offset Loss & Replication Gap** — Recovering missing records after a CDC consumer loses its checkpoint.
- **Phase 189: Debugging Lab: Partial Publish & Dirty Reads** — Fixing pipelines that expose half-written files to downstream BI queries.
- **Phase 190: Debugging Lab: Unconstrained Backfill Truncation** — Remediating backfill scripts that accidentally wiped current data.

### Part 18: Comprehensive Broken Pipeline Labs (Phase 191)
- **Phase 191: Broken Pipeline Lab Set Overview** — 32 realistic broken-pipeline incident scenarios across all engineering layers.

### Part 19: Capstone Platforms (Phases 192 - 197)
- **Phase 192: Capstone 1: Production Batch Platform** — PostgreSQL -> Parquet -> DuckDB -> dbt -> Sales Mart.
- **Phase 193: Capstone 2: Real-Time Event Platform** — Broker ingestion -> tumbling window aggregator -> real-time mart.
- **Phase 194: Capstone 3: CDC + Warehouse Platform** — Transactional WAL change capture -> warehouse replica synchronization.
- **Phase 195: Capstone 4: Modern Lakehouse Platform** — Open table format, ACID snapshot commits, schema evolution, time travel.
- **Phase 196: Capstone 5: Data Quality & Observability Platform** — Automated monitoring of freshness, volume, schema drift, quality.
- **Phase 197: Capstone 6: End-to-End Enterprise Data Platform** — Enterprise synthesis: OLTP, clickstreams, CDC, marts, quality, lineage.

### Part 20: Failure Day & Enterprise System Design (Phases 198 - 200)
- **Phase 198: Failure Day: Chaos Engineering in Data Pipelines** — Injecting concurrent failures across sources, schemas, and brokers.
- **Phase 199: Data Platform Architecture & Capacity Planning** — Capacity planning for 100+ sources, 10 TB/day, and 100+ analysts.
- **Phase 200: Final Design Challenge: Global E-Commerce Data Platform** — Comprehensive architectural design challenge.
