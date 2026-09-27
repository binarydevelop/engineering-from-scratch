# Data Engineering Comprehensive Glossary

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

### A
- **ACID**: Atomicity, Consistency, Isolation, Durability. The transaction guarantees provided by traditional databases and modern lakehouse table formats.
- **Airflow**: An open-source workflow management platform used to programmatically author, schedule, and monitor Directed Acyclic Graphs (DAGs) of tasks.
- **Arrow (Apache Arrow)**: A universal columnar in-memory data format and library that enables zero-copy sharing of analytical data between systems (e.g., Python, DuckDB, Spark).
- **At-Least-Once Delivery**: A messaging guarantee where every record is delivered at least once, but duplicate messages may occur due to network retries.
- **Atomic Replacement**: Swapping an entire table or partition in a single instantaneous metadata commit, ensuring readers never see half-written or corrupt data.

### B
- **Backfill**: Reprocessing a pipeline over a historical date range to apply updated business logic, fix a data bug, or populate a newly added table.
- **Batch Processing**: Processing accumulated data in discrete, scheduled chunks (e.g., hourly, daily) rather than continuously.
- **Broadcast Join**: An optimization in distributed SQL engines where a small dimension table is copied in full to all worker nodes, eliminating the need to shuffle the large fact table across the network.

### C
- **Change Data Capture (CDC)**: Extracting state changes (INSERT, UPDATE, DELETE) directly from a database's transaction log (WAL/binlog) and streaming them downstream.
- **Checkpoints**: Persisted metadata markers recording the last processed offset, record ID, or partition, allowing pipelines to resume safely after unexpected crashes.
- **Column Pruning**: An optimization in columnar formats where only the columns referenced in a query are scanned from disk or storage.
- **Compaction**: Merging many small files into a smaller number of appropriately sized files (e.g., 128 MB to 512 MB) to eliminate metadata overhead and speed up scans.

### D
- **DAG (Directed Acyclic Graph)**: A mathematical graph of nodes (tasks) connected by directed edges (dependencies) with no closed loops. The core model of data orchestration.
- **Data Catalog**: An inventory of an organization's data assets, capturing metadata, descriptions, schemas, owners, tags, and data quality metrics.
- **Data Contract**: A versioned specification agreed upon by producers and consumers defining schemas, SLA freshness, semantics, and quality invariants.
- **Data Lake**: A centralized repository designed to store vast quantities of raw, semi-structured, and structured data in open file formats on cheap object storage.
- **Data Lakehouse**: An architectural pattern combining the low cost and open formats of data lakes with the ACID transactions, schema evolution, and indexing of data warehouses.
- **Data Mart**: A subset of a data warehouse built and optimized for the specific reporting or analytics needs of a single business unit (e.g., Sales, Marketing).
- **Data Quality**: The measure of whether data satisfies operational and business criteria (completeness, uniqueness, validity, consistency, freshness, and accuracy).
- **dbt (data build tool)**: A transformation framework that allows engineers to write modular SQL `SELECT` queries with dependency management, testing, and documentation.
- **Dead-Letter Queue (DLQ) / Quarantine**: A dedicated storage destination where malformed or unprocessable records are routed with error metadata for post-mortem inspection.
- **Dimension Table**: In star schemas, a table containing descriptive, contextual attributes (e.g., customer name, product category, store location) used for filtering and grouping.
- **DuckDB**: An in-process, embeddable SQL OLAP database management system built for high-performance analytical queries and local vector processing.

### E
- **ELT (Extract, Load, Transform)**: A pattern where raw data is extracted from sources, loaded directly into storage or warehouse, and transformed downstream using SQL.
- **ETL (Extract, Transform, Load)**: A pattern where raw data is extracted, transformed in a dedicated compute tier before landing, and loaded into the final store.
- **Event Time**: The timestamp recorded at the exact moment an action occurred at the client or edge device.

### F
- **Fact Table**: In star schemas, a table containing numeric metrics and foreign keys referencing dimension tables, representing operational events (orders, page views).
- **Freshness**: The duration between when data occurred at the source and when it became available for querying in the analytical target.

### G
- **Grain**: The fundamental, atomic definition of what exactly one row represents in a dataset (e.g., "one row per order line item").

### I
- **Iceberg (Apache Iceberg)**: An open lakehouse table format for huge analytical datasets that tracks data files using snapshot metadata trees.
- **Idempotency**: The mathematical property of an operation whereby performing it multiple times yields the exact same state as performing it once ($f(f(x)) = f(x)$).
- **Incremental Ingestion**: Reading and processing only new or modified records since the previous watermark/checkpoint, avoiding expensive full table scans.

### L
- **Late Data**: Records that arrive at the stream processor after the time window for their event time has already closed.
- **Lineage**: The end-to-end provenance graph showing how data flows, transforms, and derives from raw upstream sources to downstream consumer dashboards.

### M
- **Medallion Architecture**: A popular lakehouse design pattern organizing data into Bronze (raw), Silver (cleaned/conformed), and Gold (business aggregates).

### O
- **OLAP (Online Analytical Processing)**: Database engines optimized for high-volume scans, aggregations, and analytical queries over billions of rows.
- **OLTP (Online Transaction Processing)**: Database engines optimized for rapid, concurrent row inserts, updates, and point lookups with strict ACID guarantees.

### P
- **Parquet (Apache Parquet)**: An open-source columnar binary storage format featuring dictionary encoding, bit-packing, run-length encoding, and embedded statistics.
- **Partition Pruning**: The query execution optimization where the engine completely skips scanning directories or partitions that do not match the query filter.
- **Partitioning**: Dividing a massive dataset into physically distinct directories or buckets based on a key (e.g., `date=2026-09-01`).
- **Processing Time**: The local machine clock time of the server or worker processing an event.

### S
- **SCD (Slowly Changing Dimension)**: Strategies for handling changes to descriptive dimension attributes over time (Type 1: overwrite; Type 2: historical version tracking with effective date ranges).
- **Schema Evolution**: The process of altering a dataset's schema over time (adding, dropping, or renaming columns) while maintaining compatibility.
- **Shuffle**: The physical process in distributed computing of repartitioning and transmitting data across the network between workers to execute `GROUP BY` or `JOIN`.
- **Skew**: An uneven distribution of data across partitions or keys, causing a single worker to process vastly more data than others, creating a long-tail bottleneck.
- **Spark (Apache Spark)**: A distributed computing engine designed for large-scale data processing with in-memory execution and structured DataFrame APIs.
- **Star Schema**: A relational modeling design featuring a central fact table surrounded by and linked to multiple denormalized dimension tables.
- **Surrogate Key**: A warehouse-generated integer or hash identifier assigned to dimension records, decoupling warehouse history from mutable source primary keys.

### W
- **WAL (Write-Ahead Log)**: An append-only disk log where database state changes are durably persisted before being applied to storage pages, serving as the basis for CDC.
- **Watermark**: In stream processing, a temporal threshold that models the processor's estimation of how far event time has progressed, determining when windows can be safely closed.
- **Window (Tumbling / Sliding)**: In stream processing, a finite boundary of time used to group and aggregate continuous events.
