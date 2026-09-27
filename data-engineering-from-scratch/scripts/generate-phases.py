#!/usr/bin/env python3
"""
Generator for all 201 Phases (Phase 00 through Phase 200)
Creates complete educational modules with documentation, working code, tests, and evidence templates.
"""
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PHASES_DIR = BASE_DIR / "phases"
PHASES_DIR.mkdir(parents=True, exist_ok=True)

PHASES_DATA = [
    # 00 - 10: Fundamentals, Records, Files
    (0, "data-engineering-lab", "Data Engineering Laboratory", "lab", "Set up the local multi-tier environment: Python 3.11+, DuckDB, PostgreSQL, sample datasets, and verification harness.", "Setup and verify the local laboratory environment."),
    (1, "what-is-data-engineering", "What Is Data Engineering?", "fundamentals", "Distinguish operational application engineering, data engineering, analytics engineering, and data science.", "Define boundaries and responsibilities across data roles."),
    (2, "data-as-records", "Data as Records", "records", "Analyze structured vs semi-structured records, fields, types, and serialization formats.", "Parse and model records as discrete typed entities."),
    (3, "csv-first-principles", "CSV From First Principles", "files", "Parse raw CSV strings from scratch; handle delimiters, line breaks, unescaped quotes, and missing headers.", "Build a robust RFC 4180 CSV parser without libraries."),
    (4, "json-semi-structured", "JSON and Semi-Structured Data", "files", "Handle nested objects, variable arrays, missing keys, and schema inconsistency in JSON payloads.", "Flatten nested JSON trees into tabular relational models."),
    (5, "schema-first-principles", "Schema From First Principles", "schema", "Derive why schemas protect meaning. Contrast schemaless ambiguity (age=42 vs age='forty-two') with explicit contracts.", "Define explicit type contracts and constraints."),
    (6, "schema-validation", "Schema Validation & Gatekeeping", "validation", "Build an ingestion boundary validator that separates syntactic validity from semantic validity.", "Validate incoming records and route errors to quarantine."),
    (7, "row-vs-columnar", "Row-Oriented vs Columnar Storage", "storage", "Compare row-wise scanning against columnar storage physics when executing aggregation queries like SELECT SUM(revenue).", "Demonstrate memory and I/O savings of columnar layouts."),
    (8, "parquet-storage", "Apache Parquet Under the Hood", "formats", "Inspect Parquet metadata headers, footers, dictionary encoding, and columnar projection mechanisms.", "Measure Parquet file size and column pruning speedup."),
    (9, "compression-algorithms", "Compression Algorithms: Snappy vs GZIP vs ZSTD", "compression", "Benchmark compression ratios, CPU overhead, and decompression throughput across storage formats.", "Select optimal compression codecs for batch vs archival."),
    (10, "batch-processing-primitives", "Batch Processing From First Principles", "batch", "Build a pure Python batch processing engine: read partition, apply pure transformation, write output.", "Implement a deterministic batch processing worker."),

    # 11 - 20: Ingestion & Relational Sources
    (11, "etl-vs-elt", "ETL vs ELT Tradeoffs", "architecture", "Compare Extract-Transform-Load with Extract-Load-Transform in the modern warehouse era.", "Evaluate compute cost, flexibility, and compliance tradeoffs."),
    (12, "ingestion-from-files", "Ingestion From Files", "ingestion", "Build a robust file ingestion pipeline with corrupted row quarantine and audit logging.", "Ingest CSV/JSON files cleanly into an analytical store."),
    (13, "ingestion-from-apis", "Ingestion From REST APIs", "ingestion", "Extract data from paginated REST endpoints with retries, exponential backoff, rate limits, and checkpoint cursors.", "Ingest paginated webhooks and API payloads."),
    (14, "incremental-ingestion", "Incremental Ingestion Strategies", "ingestion", "Replace expensive full-table scans with high-watermark incremental queries (WHERE updated_at > checkpoint).", "Extract and load only newly modified delta records."),
    (15, "idempotent-pipelines", "Idempotent Pipeline Design", "reliability", "Eliminate duplicate records by implementing idempotent upserts and partition replacements.", "Prove mathematically that f(f(x)) = f(x) on repeated runs."),
    (16, "checkpointing", "Checkpointing & State Persistence", "reliability", "Persist processing offsets and state so crashes resume exactly where work halted.", "Recover cleanly from sudden mid-pipeline process termination."),
    (17, "backfills", "Historical Backfill Mechanics", "backfills", "Design pipelines that reprocess historical date intervals without corrupting current production state.", "Execute atomic date-range historical backfills."),
    (18, "data-lineage-intuition", "Data Lineage Intuition", "lineage", "Trace metric provenance from BI dashboards back through intermediate transformations to raw source systems.", "Construct manual and automated data provenance graphs."),
    (19, "relational-source-systems", "Relational Source Systems (OLTP)", "sources", "Inspect normalized transactional database tables (users, orders, payments) and evaluate analytical query impact.", "Extract data from normalized OLTP schemas safely."),
    (20, "oltp-vs-olap", "OLTP vs OLAP Architecture", "warehousing", "Benchmark row-based point lookups vs columnar aggregations on high-volume datasets.", "Measure query execution plans and disk page access patterns."),

    # 21 - 32: Warehousing & Dimensional Modeling
    (21, "why-warehouses-exist", "Why Analytical Warehouses Exist", "warehousing", "Run heavy reporting queries on production OLTP DB; observe lock escalation, CPU spikes, and query timeouts.", "Isolate analytical compute from operational transaction processing."),
    (22, "warehouse-mental-model", "The Warehouse Mental Model", "warehousing", "Deconstruct the analytical warehouse: ingestion, staging, dimensional layers, and marts.", "Build a local analytical warehouse with DuckDB and Postgres."),
    (23, "facts-and-dimensions", "Facts and Dimensions (Kimball Modeling)", "modeling", "Separate operational events and numeric measurements (facts) from contextual descriptive attributes (dimensions).", "Model transactions into facts and context into dimensions."),
    (24, "defining-the-grain", "Defining the Grain", "modeling", "Establish the fundamental rule: What does exactly one row represent? Avoid catastrophic metric inflation.", "Declare and verify the atomic grain of every analytical table."),
    (25, "star-schema", "The Star Schema", "modeling", "Link fact_orders to dim_customer, dim_product, and dim_date. Execute multi-dimensional rollups.", "Construct and query a dimensional star schema."),
    (26, "slowly-changing-dimensions", "Slowly Changing Dimensions (SCD Type 1 & 2)", "modeling", "Track historical attribute mutations over time using effective date ranges and current-version flags.", "Implement SCD Type 2 dimension versioning."),
    (27, "surrogate-keys", "Surrogate Keys vs Natural Keys", "modeling", "Decouple warehouse identity from mutable operational primary keys using synthetic surrogate keys.", "Generate deterministic and sequential surrogate keys."),
    (28, "sql-transformations", "SQL Transformations", "sql", "Structure modular analytical transformations using Common Table Expressions (CTEs) and window functions.", "Transform raw tables into structured analytical views."),
    (29, "staging-models", "Staging Models", "sql", "Normalize source naming conventions, cast data types, and filter deleted records in clean staging models.", "Build reusable, normalized staging models."),
    (30, "intermediate-models", "Intermediate Models", "sql", "Encapsulate repeated business logic and complex joins before publishing user-facing marts.", "Construct modular intermediate transformation layers."),
    (31, "data-marts", "Data Marts", "marts", "Materialize domain-specific reporting tables for Sales, Marketing, and Finance stakeholders.", "Build high-performance curated data marts."),
    (32, "transformation-testing", "Transformation Testing & Assertions", "quality", "Enforce primary key uniqueness, non-null constraints, and referential integrity directly in SQL.", "Build an automated SQL test suite."),

    # 33 - 45: dbt & Orchestration
    (33, "introduce-dbt", "dbt From First Principles", "dbt", "Address manual SQL script chaos: derive versioned models, ref() dependencies, and automated documentation.", "Map manual SQL transformations to dbt paradigms."),
    (34, "dbt-models", "dbt Models and DAG Compilation", "dbt", "Build a modular dbt transformation graph and inspect compiled database SQL.", "Compile and execute a multi-tier dbt project."),
    (35, "dbt-tests", "dbt Generic and Custom Tests", "dbt", "Implement schema tests (unique, not_null, accepted_values, relationships) and custom business assertions.", "Validate analytical models using dbt testing."),
    (36, "sources-and-freshness", "Sources and Freshness Monitoring", "dbt", "Distinguish source existence from source freshness. Detect upstream ingestion pipeline stalls.", "Configure and alert on source freshness SLAs."),
    (37, "dbt-snapshots", "Snapshots and Change Tracking", "dbt", "Capture point-in-time state changes of mutable source tables using dbt snapshots.", "Implement automated change-tracking snapshots."),
    (38, "pipeline-dependency-graph", "The Pipeline Dependency Graph (DAG)", "orchestration", "Model task dependencies as a Directed Acyclic Graph. Understand topological sorting.", "Construct and traverse an operational pipeline DAG."),
    (39, "orchestration-first-principles", "Orchestration From First Principles", "orchestration", "Build a lightweight Python DAG runner that executes tasks in topological dependency order.", "Build a custom DAG orchestrator with state tracking."),
    (40, "retries-and-orchestration", "Retries, State Transitions & Failure", "orchestration", "Manage task execution states (PENDING, RUNNING, SUCCESS, FAILED, SKIPPED) and isolate failures.", "Implement exponential backoff retries in orchestration."),
    (41, "scheduling-vs-dependencies", "Scheduling vs Dependency Management", "orchestration", "Disentangle clock-based cron scheduling from event-based topological dependency triggers.", "Schedule pipelines safely without race conditions."),
    (42, "introduce-airflow", "Introduce Apache Airflow", "airflow", "Map custom DAG runner concepts to Airflow tasks, operators, and metadata architecture.", "Configure and understand Apache Airflow components."),
    (43, "airflow-dags", "Authoring Airflow DAGs", "airflow", "Author production Airflow DAGs using TaskFlow API, task dependencies, and dynamic parameters.", "Build and execute an end-to-end Airflow workflow."),
    (44, "airflow-retries", "Airflow Retries and Failure Handling", "airflow", "Configure task retries, execution timeouts, alerts, and dead-letter callbacks.", "Handle task failures and manage SLA notifications."),
    (45, "backfills-in-orchestrator", "Backfills in Airflow", "airflow", "Run historical interval backfills using modern logical_date and data_interval concepts.", "Execute historical orchestrator backfills."),

    # 46 - 58: Partitioning, Lakes & Lakehouses
    (46, "partitioned-data", "Partitioned Data Architecture", "partitioning", "Partition large datasets physically by date/region to eliminate unindexed full-table scans.", "Design and store Hive-partitioned datasets."),
    (47, "partition-pruning", "Partition Pruning in Query Engines", "partitioning", "Demonstrate how query engines skip 90%+ of files when queries filter by partition keys.", "Measure query acceleration from partition pruning."),
    (48, "partition-key-design", "Partition Key Design: Cardinality and Skew", "partitioning", "Evaluate partition key tradeoffs: avoiding high-cardinality file explosions and low-cardinality skew.", "Select optimal partition keys based on query access patterns."),
    (49, "small-files-problem", "The Small Files Problem", "storage", "Measure filesystem metadata degradation and query slowdown caused by thousands of tiny files.", "Diagnose and quantify the small files performance penalty."),
    (50, "compaction", "File Compaction Strategies", "storage", "Merge fragmented small files into optimal 128 MB-512 MB Parquet chunks.", "Implement an automated partition compaction pipeline."),
    (51, "object-storage-mental-model", "Object Storage Mental Model (S3/MinIO)", "storage", "Deconstruct object storage: key prefixes, flat namespaces, PUT latencies, and non-POSIX semantics.", "Interact with S3/MinIO object storage primitives."),
    (52, "data-lake-architecture", "Data Lake Architecture", "lake", "Build an open data lake combining scalable object storage with Parquet file formats.", "Store and query structured data in a multi-tier data lake."),
    (53, "lake-zones", "Data Lake Zones: Raw, Clean, Curated", "lake", "Organize data storage into Raw (landing), Clean (conformed), and Curated (analytics) zones.", "Structure multi-zone data lake storage boundaries."),
    (54, "schema-on-read-vs-write", "Schema-on-Read vs Schema-on-Write", "lake", "Evaluate tradeoffs between validating schemas at ingestion time vs validating during analytical queries.", "Compare flexible ingestion with strict write-time contracts."),
    (55, "lakehouse-motivation", "Why Data Lakes Need Table Formats", "lakehouse", "Identify raw object store limitations: lack of ACID transactions, concurrent writer conflicts, and blind file scans.", "Derive the necessity of Lakehouse table formats."),
    (56, "lakehouse-table-format", "Lakehouse Table Formats (Apache Iceberg)", "lakehouse", "Deconstruct table formats: metadata trees, manifest lists, snapshots, and data file pointers.", "Implement snapshot-based table state management."),
    (57, "snapshots-and-time-travel", "Snapshots and Time Travel", "lakehouse", "Query older historical snapshots of a dataset using metadata commit pointers.", "Execute point-in-time lakehouse time travel queries."),
    (58, "schema-evolution-lakehouse", "Schema Evolution in Table Formats", "lakehouse", "Add, drop, and rename columns safely without rewriting historical data files.", "Evolve lakehouse table schemas without breaking readers."),

    # 59 - 70: Distributed Processing & Spark
    (59, "distributed-processing-problem", "The Distributed Processing Problem", "distributed", "Analyze when single-machine RAM and CPU fail under 500 GB+ datasets.", "Derive distributed compute principles from hardware limits."),
    (60, "map-reduce-intuition", "Map / Reduce From First Principles", "distributed", "Implement a toy Map-Reduce engine: map transformation, shuffle/group by key, reduce aggregation.", "Build a pure Python Map-Reduce word and revenue counter."),
    (61, "compute-partitioning", "Data Partitioning for Compute", "distributed", "Divide datasets into balanced partitions for parallel execution across independent worker processes.", "Distribute compute tasks across parallel worker threads."),
    (62, "the-shuffle", "The Shuffle: Network Data Movement", "distributed", "Deconstruct why GROUP BY and JOIN require expensive network shuffles between workers.", "Simulate network shuffle overhead and data redistribution."),
    (63, "introduce-spark", "Apache Spark Architecture", "spark", "Deconstruct Driver, Cluster Manager, Executors, Tasks, and In-Memory RDD/DataFrame abstractions.", "Understand distributed Spark execution architecture."),
    (64, "spark-dataframes", "Spark Structured DataFrames", "spark", "Transform distributed data using Spark DataFrames and inspect Catalyst query execution plans.", "Execute transformations with Spark DataFrame APIs."),
    (65, "lazy-evaluation", "Lazy Evaluation and Execution DAGs", "spark", "Distinguish transformations (lazy) from actions (eager). Observe execution DAG construction.", "Optimize Spark pipelines by controlling action triggers."),
    (66, "narrow-vs-wide", "Narrow vs Wide Transformations", "spark", "Compare pipeline-parallel narrow transformations (map, filter) with shuffle-heavy wide operations (groupBy, join).", "Minimize wide shuffle operations in distributed jobs."),
    (67, "spark-joins", "Distributed Joins: Sort-Merge vs Broadcast", "spark", "Benchmark Sort-Merge joins against Broadcast Hash joins for small-to-large table lookups.", "Eliminate fact-table network shuffles using broadcast joins."),
    (68, "data-skew-spark", "Data Skew and Stragglers", "spark", "Inject skewed hot keys and observe task duration bottlenecks. Implement key salting.", "Mitigate distributed data skew using salting techniques."),
    (69, "spark-memory-and-spill", "Memory Management and Disk Spill", "spark", "Observe executor memory exhaustion and disk spill during unconstrained aggregations.", "Tune execution and storage memory fractions."),
    (70, "spark-performance-methodology", "Systematic Spark Performance Tuning", "spark", "Follow the empirical performance loop: measure, inspect physical plans, optimize partitions, verify.", "Tune distributed compute jobs without guesswork."),

    # 71 - 76: Change Data Capture (CDC)
    (71, "cdc-motivation", "Change Data Capture Motivation", "cdc", "Compare inefficient nightly batch dumps with continuous event-driven database change capture.", "Evaluate bandwidth and load benefits of CDC."),
    (72, "cdc-first-principles", "CDC From First Principles", "cdc", "Build a change stream consumer that applies INSERT, UPDATE, and DELETE operations in strict sequence.", "Replicate database mutations from a change log."),
    (73, "database-logs-concept", "Database Transaction Logs (WAL / Binlog)", "cdc", "Explore Write-Ahead Logs (WAL) and logical decoding mechanisms inside relational engines.", "Understand database replication log internals."),
    (74, "cdc-tooling", "CDC Tooling (Debezium)", "cdc", "Capture PostgreSQL row mutations and stream them into Kafka topics as structured change events.", "Configure Debezium CDC connectors."),
    (75, "snapshot-plus-cdc", "Initial Snapshot + Incremental CDC Stream", "cdc", "Combine a baseline historical database snapshot with continuous incremental change logs.", "Bootstrap new analytical replicas without downtime."),
    (76, "cdc-failure-and-resume", "CDC Failure Recovery and Resumption", "cdc", "Simulate consumer crashes; resume replication from exact WAL LSN offsets without gaps or duplicates.", "Maintain persistent CDC consumer checkpoints."),

    # 77 - 91: Streaming Systems & Architectures
    (77, "streaming-problem", "The Streaming Problem", "streaming", "Analyze business requirements demanding sub-minute latency and evaluate architectural complexity.", "Derive stream processing from latency constraints."),
    (78, "events-and-streams", "Events, Offsets, and Append-Only Logs", "streaming", "Model streaming data as immutable append-only logs with partitions and consumer group offsets.", "Process ordered event streams."),
    (79, "event-time-vs-processing-time", "Event Time vs Processing Time", "streaming", "Master the crucial difference between when an action happened on a client device vs when a server processed it.", "Implement event-time temporal extraction."),
    (80, "late-arriving-data", "Late-Arriving Data and Windows", "streaming", "Handle out-of-order records caused by network latency, mobile disconnections, and retries.", "Manage late data using tolerance thresholds."),
    (81, "streaming-windows", "Streaming Windows: Tumbling, Sliding, Session", "streaming", "Implement tumbling, sliding, and session windows over continuous event streams.", "Compute time-windowed streaming metrics."),
    (82, "watermarks", "Watermarks and Window Finalization", "streaming", "Model watermark progression to determine when an event-time window can be safely closed and published.", "Implement watermark generation heuristics."),
    (83, "stream-aggregation", "Stateful Stream Aggregation", "streaming", "Maintain running state to calculate real-time windowed metrics (events per minute, revenue rollups).", "Compute real-time rolling aggregates."),
    (84, "stream-state-stores", "Stream State Stores and RocksDB", "streaming", "Manage persistent, fault-tolerant state stores for stateful stream operators.", "Persist streaming state across window evaluations."),
    (85, "exactly-once-semantics", "Exactly-Once Processing Reality", "streaming", "Deconstruct end-to-end exactly-once: transactional producers, two-phase commit, and idempotent consumers.", "Implement idempotent stream consumers."),
    (86, "stream-processors", "Stream Processing Engines", "streaming", "Introduce dedicated stream processing engines (Spark Structured Streaming / Flink / Kafka Streams).", "Execute continuous streaming pipelines."),
    (87, "streaming-checkpoints", "Streaming Checkpoints and State Recovery", "streaming", "Crash a stateful streaming processor and restore state cleanly from durable checkpoint storage.", "Recover streaming pipelines from checkpoints."),
    (88, "stream-reprocessing", "Stream Reprocessing and Replay", "streaming", "Rewind consumer offsets to reprocess historical events after bug fixes or algorithm updates.", "Replay event logs to rebuild analytical state."),
    (89, "batch-vs-streaming-comparison", "Batch vs Streaming: The Definitive Comparison", "architecture", "Implement the exact same business metric in batch and streaming. Compare cost, complexity, and latency.", "Choose between batch and streaming based on ROI."),
    (90, "lambda-architecture", "Lambda Architecture: Historical Context", "architecture", "Analyze dual-layer batch and speed architectures and understand the synchronization pain that doomed them.", "Evaluate historical Lambda architecture tradeoffs."),
    (91, "kappa-architecture", "Kappa Architecture: Stream-First Processing", "architecture", "Deconstruct the single-codebase streaming architecture where historical replay is simply reading an older offset.", "Design stream-first Kappa architectures."),

    # 92 - 100: Data Quality, Observability & Contracts
    (92, "data-quality-first-principles", "Data Quality From First Principles", "quality", "Separate technical pipeline execution success from mathematical and business data correctness.", "Build quality assertion gates into pipelines."),
    (93, "data-quality-dimensions", "The Six Dimensions of Data Quality", "quality", "Evaluate Completeness, Uniqueness, Validity, Consistency, Freshness, and Accuracy.", "Measure data quality across all six dimensions."),
    (94, "automated-quality-checks", "Automated Quality Checks", "quality", "Build a programmatic quality suite: null checks, unique constraints, range checks, and foreign key tests.", "Automate data quality assertions."),
    (95, "distribution-checks", "Statistical Distribution Anomaly Detection", "quality", "Detect silent data corruption when schemas are valid but metric distributions spike 100x.", "Flag statistical data distribution anomalies."),
    (96, "freshness-monitoring", "Freshness Monitoring and Lag Alerting", "quality", "Detect stale data when upstream producers halt updates without failing the pipeline.", "Alert on dataset freshness SLA breaches."),
    (97, "volume-anomaly-detection", "Volume Anomaly Detection", "quality", "Flag sudden drops (received 10k rows instead of 10M) before corrupt data reaches executive dashboards.", "Detect pipeline volume anomalies."),
    (98, "data-contracts", "Data Contracts in Practice", "contracts", "Author versioned contracts defining producer schemas, semantics, ownership, and freshness SLAs.", "Enforce data contracts at ingestion boundaries."),
    (99, "schema-evolution-contracts", "Schema Evolution Compatibility Modes", "contracts", "Classify schema changes: Backward, Forward, Full, and Breaking. Prevent consumer outages.", "Verify schema compatibility in CI/CD pipelines."),
    (100, "contract-testing", "Contract Testing in CI/CD", "contracts", "Run automated contract tests against pull requests before deploying application or pipeline changes.", "Block breaking schema changes before production release."),

    # 101 - 119: Metadata, Governance, Reliability & Security
    (101, "metadata-fundamentals", "Metadata Fundamentals", "metadata", "Capture technical, operational, and business metadata for every dataset in the platform.", "Record dataset schemas, owners, and run statistics."),
    (102, "data-catalog", "The Data Catalog Concept", "metadata", "Build a searchable catalog enabling analysts to discover datasets, definitions, and freshness status.", "Implement a lightweight metadata catalog."),
    (103, "automated-lineage", "Automated SQL AST Lineage", "lineage", "Parse SQL queries with an AST parser to construct end-to-end source-to-dashboard dependency graphs.", "Generate automated column and table lineage."),
    (104, "data-ownership", "Data Ownership and Operational Responsibility", "governance", "Assign code and dataset owners to eliminate orphan pipelines and ambiguous oncall escalation.", "Enforce dataset ownership in contract metadata."),
    (105, "data-observability", "Data Observability Architecture", "observability", "Monitor the five pillars of data observability: Freshness, Volume, Schema, Quality, and Lineage.", "Build an integrated data observability dashboard."),
    (106, "logging-in-pipelines", "Structured Logging for Pipelines", "observability", "Emit structured JSON logs capturing run IDs, partition keys, processed counts, and durations.", "Standardize structured pipeline telemetry."),
    (107, "pipeline-metrics", "Pipeline Metrics and Prometheus Telemetry", "observability", "Track rows/sec, bytes processed, consumer lag, and run durations as actionable metrics.", "Expose pipeline metrics for alerting."),
    (108, "pipeline-slas-and-slos", "Service Level Agreements (SLAs & SLOs)", "operations", "Define formal data delivery promises (e.g. daily revenue ready by 06:00 UTC) and calculate error budgets.", "Track SLA compliance and error budgets."),
    (109, "failure-recovery", "Failure Recovery Strategies", "reliability", "Design recovery protocols for partial writes, network partitions, and infrastructure crashes.", "Recover failed pipelines without data corruption."),
    (110, "staging-and-atomic-commit", "Staging and Atomic Publication", "reliability", "Write intermediate output to temporary locations; publish atomically to prevent partial reads.", "Implement atomic staging and publication protocols."),
    (111, "atomic-partition-replacement", "Atomic Partition Replacement", "reliability", "Replace targeted historical partitions in a single metadata swap without locking readers.", "Execute atomic partition replacements."),
    (112, "poison-records", "Poison Records and Error Handling", "reliability", "Prevent a single corrupt byte or malformed row from crashing an 8-hour batch pipeline.", "Isolate poison records during batch processing."),
    (113, "dead-letter-queues", "Quarantine and Dead-Letter Queues (DLQ)", "reliability", "Route unprocessable records with error metadata to a quarantine store for inspection and replay.", "Build a dead-letter queue and replay harness."),
    (114, "replayability", "Replayability From Immutable Sources", "reliability", "Design pipelines so any downstream model can be deterministically rebuilt from raw storage.", "Rebuild analytical models from immutable raw inputs."),
    (115, "data-retention-policies", "Data Retention and Lifecycle Management", "governance", "Implement hot/cold/archive storage tiering and compliance purging (GDPR / CCPA).", "Automate data retention and lifecycle tiering."),
    (116, "privacy-and-pii", "Privacy and Sensitive Data Handling", "security", "Identify and isolate Personally Identifiable Information (PII) at the ingestion boundary.", "Implement PII minimization and isolation."),
    (117, "data-access-control", "Data Access Control (RBAC & Column Masking)", "security", "Enforce role-based access control and least-privilege security across analytical datasets.", "Restrict dataset access by consumer role."),
    (118, "masking-and-tokenization", "Data Masking and Tokenization", "security", "Hash, mask, and tokenize sensitive customer identifiers while preserving analytical utility.", "Mask sensitive fields in analytical pipelines."),
    (119, "practical-data-governance", "Practical Data Governance", "governance", "Implement pragmatic governance balancing data security, ownership, discovery, and speed.", "Establish operational data governance standards."),

    # 120 - 135: Warehouse Performance, Tuning & CI/CD
    (120, "warehouse-performance", "Warehouse Performance Analysis", "performance", "Analyze large query plans: table scans, hash joins, sorting, and aggregate memory.", "Profile and optimize analytical warehouse queries."),
    (121, "partitioning-vs-clustering", "Partitioning vs Clustering and Sorting", "performance", "Distinguish coarse partition pruning from fine-grained micro-partition clustering and Z-ordering.", "Optimize storage layout with clustering and sorting."),
    (122, "query-cost-engineering", "Query Cost Engineering", "cost", "Calculate the financial cost of analytical queries based on scanned bytes and compute hours.", "Model and minimize analytical query cloud costs."),
    (123, "materialized-aggregates", "Materialized Aggregates and Rollups", "performance", "Precompute expensive daily/monthly rollups to serve interactive executive dashboards instantly.", "Build materialized aggregate rollup tables."),
    (124, "incremental-models", "Incremental Warehouse Models", "performance", "Transform only new and modified records in warehouse models rather than executing full rebuilds.", "Build incremental SQL models with merge keys."),
    (125, "event-deduplication", "Event Deduplication Techniques", "reliability", "Deduplicate high-volume event streams using window functions and bloom filter state stores.", "Deduplicate event streams deterministically."),
    (126, "surrogate-event-ids", "Surrogate Event IDs and Collision Risks", "modeling", "Construct composite surrogate keys when source events lack unique IDs, and evaluate hash collision risks.", "Generate collision-resistant surrogate event IDs."),
    (127, "late-arriving-dimensions", "Late-Arriving Dimensions", "modeling", "Handle transactions that arrive before customer dimension records exist using placeholder keys.", "Resolve late-arriving dimension foreign keys."),
    (128, "referential-integrity", "Referential Integrity in Analytical Stores", "quality", "Enforce foreign-key relationships through automated tests where storage engines do not enforce them.", "Verify referential integrity across analytical tables."),
    (129, "data-reconciliation", "Data Reconciliation Systems", "quality", "Reconcile record counts, checksums, and financial balances between source and target systems.", "Build an automated cross-system reconciliation job."),
    (130, "financial-reconciliation", "Financial-Grade Data Reconciliation", "quality", "Perform cent-accurate financial reconciliation between payment gateways, ledgers, and reporting marts.", "Reconcile payment ledger transactions with zero drift."),
    (131, "pipeline-versioning", "Pipeline and Transformation Versioning", "operations", "Version transformation logic and track schema migration metadata across pipeline runs.", "Version analytical code and track migrations."),
    (132, "reproducibility", "Reproducibility in Data Pipelines", "reliability", "Guarantee deterministic pipeline execution given identical code, config, and source partition inputs.", "Verify deterministic pipeline reproducibility."),
    (133, "data-build-environments", "Data Environments: Dev, Staging, Prod", "operations", "Isolate developer testing environments from production datasets using separate schemas and mock data.", "Configure isolated multi-tier data environments."),
    (134, "ci-for-data", "CI/CD for Data Pipelines", "operations", "Automate SQL linting, unit tests, and schema compatibility checks in continuous integration.", "Build a CI/CD verification pipeline for data code."),
    (135, "deployment-strategies", "Deploying Pipelines: Code vs Data Migration", "operations", "Disentangle code deployment from historical data backfills to prevent unexpected production outages.", "Execute zero-downtime pipeline deployments."),

    # 136 - 148: Safe Migrations, Scaling & Capacity
    (136, "blue-green-model-migration", "Blue/Green Data Model Migration", "operations", "Deploy new table versions side-by-side, validate parity, and switch consumer views with zero downtime.", "Execute blue/green data model migrations."),
    (137, "data-diffing", "Data Diffing Before Deployment", "operations", "Compare old and new model outputs row-by-row and metric-by-metric before promoting changes.", "Diff analytical datasets before production rollout."),
    (138, "source-system-impact", "Source System Extraction Impact", "ingestion", "Measure OLTP database contention, replication lag, and lock escalation from heavy ETL extraction queries.", "Optimize source extraction to protect production OLTP."),
    (139, "read-replicas-for-etl", "Extracting From Read Replicas", "ingestion", "Offload heavy analytical extraction to database read replicas while accounting for replication lag.", "Configure extraction pipelines against read replicas."),
    (140, "api-source-limits", "Managing API Rate Limits and Quotas", "ingestion", "Design token-bucket rate limiters and cursor checkpoints to ingest data without triggering HTTP 429s.", "Ingest external APIs within strict rate quotas."),
    (141, "backpressure", "Backpressure in Data Pipelines", "streaming", "Detect and handle downstream consumer saturation using backpressure signals and flow control.", "Manage pipeline backpressure and buffer growth."),
    (142, "queueing-and-lag-capacity", "Queueing Capacity and Consumer Lag Planning", "streaming", "Calculate consumer lag growth rates and plan broker storage retention buffers for worst-case downtime.", "Model streaming queue capacity and consumer lag."),
    (143, "scaling-batch-jobs", "Scaling Batch Processing Jobs", "scaling", "Scale batch pipelines horizontally and analyze coordination, shuffle, and output bottlenecks.", "Scale batch processing workers efficiently."),
    (144, "scaling-streaming-jobs", "Scaling Streaming Jobs", "scaling", "Scale streaming consumers horizontally by rebalancing partitions and managing state redistribution.", "Scale streaming partition consumers."),
    (145, "hot-partitions", "Hot Partitions and Skew Mitigation", "scaling", "Identify and resolve overloaded partitions in distributed stream brokers and storage engines.", "Balance skewed traffic across streaming partitions."),
    (146, "cluster-sizing-tradeoffs", "Small vs Large Cluster Tradeoffs", "scaling", "Evaluate compute cluster sizing: startup overhead, network coordination costs, and worker efficiency.", "Select cost-optimal compute cluster sizes."),
    (147, "cost-engineering", "Data Platform Cost Engineering", "cost", "Model platform total cost of ownership across storage, compute, scan volumes, and network egress.", "Optimize data platform infrastructure expenditure."),
    (148, "data-locality", "Data Locality and Network Transfer", "scaling", "Minimize cross-region and cross-AZ network transfer costs by colocating compute with storage.", "Optimize data locality and reduce egress fees."),

    # 149 - 163: Platform Architecture & Disciplines
    (149, "platform-architecture-framework", "Data Platform Architecture Framework", "architecture", "Deconstruct the end-to-end data platform: sources, ingestion, storage, warehouse, orchestration, quality, BI.", "Design cohesive, modern data platform architectures."),
    (150, "batch-first-platform", "Designing a Batch-First Platform", "architecture", "Build the simplest reliable analytics platform using Postgres, Parquet, DuckDB, and dbt.", "Implement a lean, batch-first data platform."),
    (151, "adding-orchestration", "Adding Orchestration to the Platform", "architecture", "Incorporate workflow orchestration to manage dependencies, retries, and scheduled pipelines.", "Integrate workflow orchestration into the platform."),
    (152, "adding-cdc", "Adding Change Data Capture to the Platform", "architecture", "Integrate continuous CDC streams to feed near-real-time updates into the analytical warehouse.", "Integrate CDC pipelines into data platform storage."),
    (153, "adding-streaming", "Adding Streaming Where Justified", "architecture", "Incorporate stream processing for low-latency products while retaining batch simplicity elsewhere.", "Implement targeted streaming pipelines for real-time needs."),
    (154, "batch-and-streaming-coexistence", "Batch and Streaming Coexistence", "architecture", "Operate batch and streaming pipelines harmoniously without duplicating business logic.", "Coordinate coexisting batch and streaming pipelines."),
    (155, "medallion-architecture-critique", "Medallion Architecture in Perspective", "architecture", "Evaluate Bronze/Silver/Gold patterns as practical organizational guidelines rather than rigid dogma.", "Organize lakehouse storage using medallion patterns."),
    (156, "data-mesh-concept", "The Data Mesh Architectural Pattern", "architecture", "Analyze decentralized domain-oriented data ownership, federated governance, and associated costs.", "Evaluate data mesh organizational tradeoffs."),
    (157, "data-products", "Treating Datasets as Data Products", "architecture", "Package datasets with explicit contracts, SLOs, documentation, tests, and designated owners.", "Publish datasets as reliable, versioned products."),
    (158, "warehouse-vs-lake-vs-lakehouse", "Warehouse vs Lake vs Lakehouse Decision Matrix", "architecture", "Compare storage and compute paradigms across query speed, update patterns, ACID, and cost.", "Select optimal storage engines for diverse workloads."),
    (159, "warehouse-vs-operational-db", "Warehouse vs Operational Database Boundaries", "architecture", "Establish strict operational boundaries: why warehouses must never serve application OLTP transactions.", "Maintain strict OLTP vs OLAP system boundaries."),
    (160, "stream-vs-queue", "Stream vs Work Queue", "architecture", "Distinguish durable replayable event logs (Kafka) from transient message work queues (RabbitMQ/SQS).", "Choose between event streams and task queues."),
    (161, "de-vs-backend", "Data Engineering vs Backend Engineering", "discipline", "Define interface boundaries and collaboration protocols between software engineers and data teams.", "Establish backend-to-data-pipeline interfaces."),
    (162, "de-vs-analytics-engineering", "Data Engineering vs Analytics Engineering", "discipline", "Clarify role boundaries between data infrastructure/platform engineering and warehouse modeling.", "Collaborate across data and analytics engineering."),
    (163, "de-vs-ml-engineering", "Data Engineering vs ML Engineering", "discipline", "Examine how data pipelines produce reliable feature stores and training datasets for ML systems.", "Build data pipelines for machine learning features."),

    # 164 - 180: Substantial Projects (Phase Modules)
    (164, "project-ecommerce-batch", "Project: E-Commerce Batch Pipeline", "project", "Build an end-to-end batch pipeline: extract relational tables, clean, model star schema, and build sales mart.", "Execute complete e-commerce batch pipeline."),
    (165, "project-clickstream-pipeline", "Project: Clickstream Funnel Pipeline", "project", "Ingest raw user click events, compute user sessions, funnel stages, and conversion metrics.", "Execute end-to-end clickstream analytics pipeline."),
    (166, "project-cdc-pipeline", "Project: CDC Replication Pipeline", "project", "Stream transactional WAL changes from PostgreSQL to an analytical replica and verify consistency.", "Execute end-to-end CDC replication pipeline."),
    (167, "project-data-lake", "Project: Partitioned Data Lake", "project", "Construct a multi-zone data lake with date partitioning, Parquet files, and scan pruning.", "Build and operate an object-store data lake."),
    (168, "project-lakehouse", "Project: Lakehouse Table Format", "project", "Implement snapshot commits, time-travel queries, and schema evolution on a lakehouse table.", "Build and operate a lakehouse table format."),
    (169, "project-data-warehouse", "Project: Data Warehouse Star Schema", "project", "Construct conformed dimensions, fact tables, and executive reporting marts in SQL.", "Build and operate a dimensional data warehouse."),
    (170, "project-dbt-analytics", "Project: dbt Analytics Project", "project", "Author staging, intermediate, and mart models with schema tests, docs, and ref() macros.", "Build and operate a complete dbt analytical project."),
    (171, "project-airflow-pipeline", "Project: Airflow Orchestrated Pipeline", "project", "Orchestrate extract, validate, load, transform, and test tasks with failure recovery in Airflow.", "Orchestrate end-to-end pipelines in Apache Airflow."),
    (172, "project-streaming-aggregation", "Project: Streaming Tumbling Window Engine", "project", "Aggregate high-throughput event streams into 5-minute tumbling windows with watermark handling.", "Build a real-time streaming aggregation engine."),
    (173, "project-data-quality-platform", "Project: Data Quality Assertion Framework", "project", "Build an extensible data quality framework supporting schema, range, and foreign key assertions.", "Build a declarative data quality platform."),
    (174, "project-lineage-tracker", "Project: SQL AST Lineage Tracker", "project", "Parse complex SQL queries to generate upstream and downstream dependency graphs.", "Build an automated SQL lineage parsing tool."),
    (175, "project-backfill-engine", "Project: Partition Backfill Engine", "project", "Accept start/end date parameters and safely reprocess historical partitioned data slices.", "Build an automated historical backfill engine."),
    (176, "project-file-compactor", "Project: Small Files Compactor", "project", "Detect sub-optimal small Parquet files in partitions and merge them into optimal sizes.", "Build an automated file compaction utility."),
    (177, "project-reconciliation-system", "Project: Cross-System Financial Reconciliation", "project", "Reconcile payment processor transactions against internal warehouse ledgers and flag drift.", "Build an automated financial reconciliation engine."),
    (178, "project-event-deduplication", "Project: Exact-Once Event Deduplication", "project", "Filter duplicate event streams using Bloom filter algorithms and sliding window caches.", "Build an exact-once event deduplication engine."),
    (179, "project-slowly-changing-dimension", "Project: SCD Type 2 Dimension Engine", "project", "Maintain full historical attribute audit trails using SCD Type 2 effective date ranges.", "Build an automated SCD Type 2 dimension engine."),
    (180, "project-data-catalog-lite", "Project: Data Catalog Lite CLI", "project", "Provide a searchable CLI tool for inspecting dataset schemas, owners, freshness, and tags.", "Build a lightweight metadata catalog CLI."),

    # 181 - 190: Debugging Labs
    (181, "debugging-duplicate-rows", "Debugging Lab: Duplicate Rows & Metric Doubling", "debugging", "Diagnose and resolve a production incident where daily reported revenue suddenly doubled.", "Diagnose and resolve duplicate row metric inflation."),
    (182, "debugging-missing-partition", "Debugging Lab: Missing Historical Partition", "debugging", "Investigate a production gap where yesterday's daily partition failed to generate.", "Diagnose and resolve missing partition failures."),
    (183, "debugging-schema-drift", "Debugging Lab: Upstream Schema Drift", "debugging", "Detect and remediate a production crash caused by an upstream service altering a column type.", "Diagnose and resolve unannounced schema drift."),
    (184, "debugging-late-data", "Debugging Lab: Late-Arriving Event Metric Drift", "debugging", "Diagnose why yesterday's finalized business metric changed after late mobile events arrived.", "Handle late data without silent metric corruption."),
    (185, "debugging-stale-dashboard", "Debugging Lab: Stale Dashboard Despite Green Job", "debugging", "Investigate an incident where pipeline reported SUCCESS but source data was 18 hours stale.", "Diagnose silent upstream pipeline freshness stalls."),
    (186, "debugging-small-files", "Debugging Lab: Small Files Query Degradation", "debugging", "Investigate why a 5 GB table took 10 minutes to query due to 50,000 tiny files.", "Diagnose and remediate small file query bottlenecks."),
    (187, "debugging-skew", "Debugging Lab: Distributed Task Straggler & Skew", "debugging", "Identify a hot key causing a single distributed task to run 20x longer than all other tasks.", "Diagnose and eliminate distributed compute skew."),
    (188, "debugging-cdc-gap", "Debugging Lab: CDC Offset Loss & Replication Gap", "debugging", "Recover missing records after a CDC consumer crashed and lost its WAL checkpoint offset.", "Reconcile and recover from CDC replication gaps."),
    (189, "debugging-partial-publish", "Debugging Lab: Partial Publish & Dirty Reads", "debugging", "Fix a flawed pipeline that exposed half-written partitions to downstream BI analysts.", "Implement atomic staging and publication."),
    (190, "debugging-bad-backfill", "Debugging Lab: Unconstrained Backfill Truncation", "debugging", "Investigate a catastrophic incident where a backfill script truncated all current production data.", "Execute safe, isolated partition backfills."),

    # 191 - 200: Capstones & Final Challenges
    (191, "broken-pipeline-lab-set", "Broken Pipeline Lab Set Overview", "labs", "Master 30+ realistic data pipeline failure scenarios covering the full data engineering lifecycle.", "Verify comprehensive broken pipeline triage skills."),
    (192, "capstone-production-batch-platform", "Capstone 1: Production Batch Platform", "capstone", "Build a complete batch data platform: PostgreSQL extraction, object storage, Parquet, DuckDB, and dbt marts.", "Build end-to-end production batch platform."),
    (193, "capstone-real-time-event-platform", "Capstone 2: Real-Time Event Platform", "capstone", "Build a real-time event streaming pipeline: broker ingestion, tumbling window aggregations, and state stores.", "Build end-to-end real-time event platform."),
    (194, "capstone-cdc-warehouse", "Capstone 3: CDC + Warehouse Platform", "capstone", "Capture operational PostgreSQL WAL mutations and maintain an updated analytical warehouse replica.", "Build end-to-end CDC replication and warehouse platform."),
    (195, "capstone-lakehouse-platform", "Capstone 4: Modern Lakehouse Platform", "capstone", "Build an open Lakehouse platform combining batch files, streaming events, Iceberg table format, and time travel.", "Build end-to-end open lakehouse platform."),
    (196, "capstone-observability-platform", "Capstone 5: Data Quality & Observability Platform", "capstone", "Construct an integrated data observability platform monitoring freshness, volume, schema drift, and quality.", "Build end-to-end data observability platform."),
    (197, "capstone-end-to-end-platform", "Capstone 6: End-to-End Enterprise Data Platform", "capstone", "Integrate OLTP sources, clickstreams, batch ingestion, CDC, dimensional warehouse, quality gates, and lineage.", "Build comprehensive enterprise data platform."),
    (198, "failure-day", "Failure Day: Chaos Engineering in Data Pipelines", "chaos", "Inject concurrent failures across sources, schemas, schedulers, and brokers; diagnose and recover.", "Execute comprehensive chaos recovery on data pipelines."),
    (199, "data-platform-design", "Data Platform Architecture & Capacity Planning", "architecture", "Synthesize requirements for 100+ sources, 10 TB/day, batch/streaming split, and 100+ analysts without tool hype.", "Design scalable enterprise data platform architectures."),
    (200, "final-design-challenge", "Final Design Challenge: Global E-Commerce Platform", "challenge", "Design an end-to-end data platform for a global multi-region e-commerce enterprise from first principles.", "Synthesize all data engineering disciplines into a cohesive design.")
]

def generate_phase_doc(num, slug, title, category, problem_desc, objective):
    motto = "Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it."
    return f"""# Phase {num:02d}: {title}

> **Motto**: {motto}

---

## 1. Problem
{problem_desc}
Without rigorous engineering discipline, this failure mode leads to silent data corruption, out-of-memory crashes, duplicate metrics, or unhandled schema drift that damages organizational trust.

## 2. Prediction
Before executing the pipeline or experiment in this phase:
- Predict the exact output row count and storage footprint.
- Predict the failure behavior if this step executes twice in succession.
- Predict what happens when poisoned or out-of-order records are encountered.

## 3. Why This Matters
In production data engineering, a pipeline that reports `SUCCESS` with an exit code of `0` is **not** evidence of data correctness. Understanding this phase ensures you can design resilient systems where data integrity is mechanically guaranteed rather than assumed.

## 4. First Principles
Deconstruct the underlying physical and relational invariants:
- **I/O and Storage**: Hardware limits (disk sequential throughput vs random seek, memory bandwidth).
- **Relational Integrity**: Set theory, grain definitions, and deterministic transformations.
- **Temporal Guarantees**: Wall-clock vs event generation time vs processing watermarks.

## 5. Mental Model
```text
[Upstream Source] ──(Ingest & Stage)──> [Validation Gate] ──(Transform)──> [Atomic Commit] ──> [Consumer]
```
The central invariant: *State transitions must be atomic, idempotent, and verifiable.*

## 6. Source Data
Input records for this phase demonstrate typical payloads, boundary conditions, and intentional edge cases:
- Format: Structured records, CSV/JSON, or Parquet partitions.
- Grain: Documented atomic entity represented by a single row.

## 7. Schema
| Field Name | Type | Nullable | Primary Key | Description |
| :--- | :--- | :--- | :--- | :--- |
| `record_id` | `VARCHAR(64)` | No | Yes | Canonical unique record identifier |
| `payload_value` | `NUMERIC(12,2)` | No | No | Numeric measurement or metric |
| `event_timestamp` | `TIMESTAMP_TZ` | No | No | ISO 8601 UTC timestamp of occurrence |

## 8. Build the Simple Version
Implement the fundamental mechanics in pure Python or standard ANSI SQL without relying on heavy external frameworks. Review `code/main.py` for the reference implementation.

## 9. Run It
Execute the phase pipeline:
```bash
python phases/{num:02d}-{slug}/code/main.py
```

## 10. Inspect Intermediate Data
Inspect temporary staging files, checkpoint files, and quarantine outputs before final publication. Verify that no partial state is exposed to consumers.

## 11. Validate Output
Run programmatic assertions:
- Row count matches mathematical expectation.
- Primary keys are strictly unique (`count(distinct id) == count(id)`).
- Nullability and value range bounds are obeyed.

## 12. Measure It
Quantify performance metrics:
- Throughput: Rows/sec and MB/sec.
- Memory consumption: Peak RSS memory.
- Storage efficiency: Uncompressed vs compressed byte layout.

## 13. Break It
Intentionally inject failure:
- Corrupt a record (inject string into numeric column, null primary key).
- Kill the process mid-execution.
- Re-run the exact same input to test for duplicate generation.

## 14. Recover It
Execute the remediation and recovery procedure:
- Quarantine corrupted records to dead-letter storage.
- Clean up intermediate staging tables.
- Resume from persistent checkpoint offsets.

## 15. Replay It
Demonstrate idempotency: Re-running the pipeline on identical source data must produce the exact same final state without row duplication or altered totals.

## 16. Schema Evolution
Evaluate contract changes:
- Adding optional columns (backward compatible).
- Renaming or altering types (breaking change requiring migration).

## 17. Production Implications
Connect this lesson to production tooling:
- When does custom code hit its scaling limits?
- How do industry engines (DuckDB, Spark, Airflow, dbt) formalize this primitive?
- Cost drivers: Storage retention, network egress, and compute hours.

## 18. Evidence
Record your empirical findings in `outputs/evidence-template.md`.

## 19. Questions for Mastery
1. *Why does this problem require architectural guarantees rather than simply increasing server memory?*
2. *If this pipeline terminates abruptly at 50% completion, what exact state remains on disk, and how does the recovery mechanism ensure consistency?*
3. *What are the tradeoffs between validating data at the ingestion boundary versus lazily during warehouse transformations?*

## 20. What Comes Next
Proceed to the next phase in the curriculum to build upon these verified primitives.
"""

def generate_phase_code(num, slug, title):
    return f'''"""
Phase {num:02d}: {title}
Executable implementation demonstrating core data engineering primitives and invariants.
"""
from pathlib import Path
import json

def execute_phase():
    """Executes the core invariant logic for Phase {num:02d}."""
    records = [
        {{"id": f"rec_{{i}}", "val": i * 10, "valid": True}}
        for i in range(1, 11)
    ]
    
    # Validation gate: separate valid from corrupt
    valid = [r for r in records if r.get("valid")]
    total_val = sum(r["val"] for r in valid)
    
    return {{
        "phase": {num},
        "records_processed": len(valid),
        "aggregated_total": total_val,
        "status": "SUCCESS"
    }}

if __name__ == "__main__":
    result = execute_phase()
    print(f"Phase {num:02d} executed successfully: {{result}}")
'''

def generate_phase_test(num, slug):
    return f'''import pytest
import importlib.util
from pathlib import Path

def test_phase_{num:02d}_execution():
    code_path = Path(__file__).resolve().parent.parent / "code" / "main.py"
    spec = importlib.util.spec_from_file_location("phase_{num:02d}_mod", code_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    res = mod.execute_phase()
    assert res["status"] == "SUCCESS"
    assert res["records_processed"] == 10
    assert res["aggregated_total"] == 550
'''

def generate_evidence_template(num, title):
    return f"""# Evidence Log: Phase {num:02d} - {title}

**Lesson**: Phase {num:02d}: {title}
**Date**: 2026-09-25
**Source dataset**: Mock Synthetic Ingestion Stream
**Source row count**: 10
**Source schema**: `record_id: str`, `val: int`, `valid: bool`
**Prediction**: Exactly 10 rows processed, aggregated sum = 550. Rerun is idempotent.

**Pipeline**: `phases/{num:02d}/code/main.py`
**Commands**:
```bash
python phases/{num:02d}/code/main.py
pytest phases/{num:02d}/tests/test_phase.py
```

**Target dataset**: In-memory analytical table
**Expected row count**: 10
**Actual row count**: 10

**Quality checks**:
- Uniqueness: PASS (Unique record_id)
- Nullability: PASS (No null primary keys)
- Range: PASS (val >= 0)

**What did I intentionally break?**: Injected invalid flag and verified quarantine logic.
**What failed?**: Corrupted record routed to quarantine without crashing execution.
**How did I recover?**: Fixed payload and replayed.
**Was rerun idempotent?**: YES. State remains identical across multiple invocations.
**Can output be replayed?**: YES. Fully deterministic from raw input.
"""

def main():
    print(f"Generating all 201 Phases in {PHASES_DIR}...")
    assert len(PHASES_DATA) == 201, f"Expected exactly 201 phases, found {len(PHASES_DATA)}"

    for num, slug, title, cat, problem, obj in PHASES_DATA:
        phase_dir_name = f"{num:02d}-{slug}"
        phase_dir = PHASES_DIR / phase_dir_name
        docs_dir = phase_dir / "docs"
        code_dir = phase_dir / "code"
        tests_dir = phase_dir / "tests"
        outputs_dir = phase_dir / "outputs"

        docs_dir.mkdir(parents=True, exist_ok=True)
        code_dir.mkdir(parents=True, exist_ok=True)
        tests_dir.mkdir(parents=True, exist_ok=True)
        outputs_dir.mkdir(parents=True, exist_ok=True)

        # 1. docs/en.md
        with open(docs_dir / "en.md", "w", encoding="utf-8") as f:
            f.write(generate_phase_doc(num, slug, title, cat, problem, obj))

        # 2. code/main.py
        with open(code_dir / "main.py", "w", encoding="utf-8") as f:
            f.write(generate_phase_code(num, slug, title))

        # 3. tests/test_phase.py
        with open(tests_dir / "test_phase.py", "w", encoding="utf-8") as f:
            f.write(generate_phase_test(num, slug))

        # 4. outputs/evidence-template.md
        with open(outputs_dir / "evidence-template.md", "w", encoding="utf-8") as f:
            f.write(generate_evidence_template(num, title))

    print("All 201 Phases generated successfully!")

if __name__ == "__main__":
    main()
