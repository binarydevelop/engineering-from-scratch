# Technology Versions & Ecosystem Reference

> **Course Policy**: Never begin with tools. Tools are concrete implementations of fundamental data engineering primitives. This document records the tested versions and reference specifications across all ecosystem components used throughout the curriculum.

---

## 1. Core Runtime & Language Specification

| Component | Target Version | Baseline Minimum | Role & Rationale |
| :--- | :--- | :--- | :--- |
| **Python** | `3.14.x` / `3.12+` | `3.11+` | Primary programming language. Used for record parsers, stream simulators, quality engines, and DAG runners. |
| **SQL** | `SQL:2016+` | `ANSI SQL-92` | First-class transformation language. Window functions, CTEs, aggregations, relational algebra. |
| **Bash / POSIX Shell** | `Bash 5.2+` / `Zsh` | `POSIX` | Operational orchestration, cron triggers, environment checks, container management. |

---

## 2. Engines & Storage Layers

| Technology | Reference Version | Ecosystem Status | Role in Curriculum |
| :--- | :--- | :--- | :--- |
| **DuckDB** | `1.1.x` - `1.5.x` | Active Stable | In-process columnar OLAP engine. Used for fast local vector execution, SQL transformations, and Parquet scanning. |
| **PostgreSQL** | `16.x` / `17.x` | Active Stable | Industry-standard transactional OLTP database and reference SQL relational warehouse. |
| **PyArrow / Apache Arrow** | `17.x` - `25.x` | Active Stable | In-memory columnar format and Parquet reader/writer primitives. |
| **Apache Iceberg** | `1.6.x` | Open Table Format Standard | Reference Lakehouse table format: snapshots, metadata tree, schema evolution, time-travel. |
| **Apache Spark** | `3.5.x` / `4.0 preview` | Active Stable | Distributed computing reference model: Driver/Executor, narrow vs wide transformations, shuffle, Catalyst optimizer. |
| **Apache Airflow** | `2.10.x` / `3.0` | Active Stable | Pipeline orchestration reference: DAGs, TaskFlow, logical date intervals, retry backoff, sensors. |
| **Apache Kafka** | `3.8.x` | Active Stable | Distributed append-only event log reference: partitions, offsets, consumer groups, retention. |
| **dbt-core** | `1.8.x` - `1.9.x` | Active Stable | Analytical SQL transformation framework: `ref()`, `source()`, compilation, lineage generation, tests. |
| **MinIO** | `RELEASE.2024-08+` | Active Stable | Local S3-compatible object storage server for lake and lakehouse experiments. |
| **Debezium** | `2.7.x` | Active Stable | Log-based Change Data Capture (CDC) reference implementation for database WAL stream capture. |

---

## 3. Python Package Ecosystem

```toml
[dependencies]
duckdb = ">=1.1.0"
pyarrow = ">=17.0.0"
pydantic = ">=2.8.0"
sqlparse = ">=0.5.0"
tabulate = ">=0.9.0"
python-dotenv = ">=1.0.1"
pytest = ">=8.3.0"
rich = ">=13.8.0"
psycopg = ">=3.2.0"
```

---

## 4. Open File Formats Specification

- **Apache Parquet**: Apache Parquet 2.x encoding format (dictionary encoding, run-length encoding, bit-packing, Snappy, GZIP, and ZSTD compression codecs, Thrift file metadata header/footer).
- **CSV (RFC 4180)**: Character-separated values, header preservation, quote escaping (`"`), delimiter handling (`,`, `\t`, `|`).
- **JSON / JSON Lines (JSONL / NDJSON)**: Semi-structured nested objects, RFC 8259, stream-delimited newline records.
- **Apache Avro**: Binary row-oriented serialization format with compact binary encoding and schema definition.

---

## 5. Architectural Version Compatibility Matrix

| Engine | Storage Format | Metastore / Catalog | Protocol |
| :--- | :--- | :--- | :--- |
| **DuckDB** | Local Parquet / In-Memory | DuckDB internal / File catalog | Direct C++ API / Arrow IPC |
| **PostgreSQL** | Heap Pages (8KB blocks), WAL | System Catalogs (`pg_catalog`) | Postgres wire protocol v3 |
| **Spark** | Parquet / Iceberg / ORC | Iceberg REST Catalog / Hive Metastore | Spark RPC / Arrow IPC |
| **Airflow** | PostgreSQL Metadata DB | Metadata tables (`dag`, `task_instance`) | SQLAlchemy / REST API |
| **Kafka** | On-disk segment log files (`.log`, `.index`) | KRaft (Kafka Raft Metadata) | Kafka binary wire protocol |

---

## 6. Deprecation Notices & Modern Terminology Guarantees

1. **Airflow Execution Date**: Deprecated since Airflow 2.2. In this curriculum, we strictly use modern `data_interval_start`, `data_interval_end`, and `logical_date` terminology.
2. **Spark RDD First**: RDDs are treated as historical low-level primitives. The modern DataFrame and Structured Streaming engine with Catalyst optimization is the primary pedagogical abstraction.
3. **Kafka ZooKeeper**: Deprecated in Kafka 3.x and removed in 4.x. All Kafka architecture references assume modern **KRaft** (Kafka Raft) consensus.
4. **Lakehouse vs Medallion**: Medallion architecture (`bronze`/`silver`/`gold`) is taught as an optional organizational pattern popularized by Databricks, not an immutable standard. We ground lakehouse concepts in the functional layers: `raw`, `cleaned`, and `curated`.
