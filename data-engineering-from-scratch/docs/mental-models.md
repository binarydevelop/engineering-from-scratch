# Core Mental Models of Data Engineering

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

Data engineering is fundamentally governed by a small set of mechanical and mathematical mental models. Master these primitives, and every new tool or framework becomes trivial to deconstruct.

---

## 1. The Data Movement Pipeline as a Pure Function

```text
Target_State[T] = F(Source_Data[T], Transformation_Logic, Configuration)
```

The gold standard of batch data engineering is treating a pipeline as a deterministic pure function:
- **Given the exact same input partition** and the exact same code version, the pipeline must produce the **exact same output dataset**.
- It has no hidden side effects (e.g., relying on `datetime.now()` inside transformation logic instead of explicit logical execution dates).
- This pure function model allows effortless backfills, historical replays, and local testing without touching production databases.

---

## 2. The Analytical Funnel (Layered Modeling Architecture)

```text
    ┌──────────────────────────────────────────────┐
    │              RAW / BRONZE ZONE               │
    │  - Immutable landing copy of source files    │
    │  - Retains all raw formats (JSON, CSV, WAL)  │
    └──────────────────────┬───────────────────────┘
                           ▼
    ┌──────────────────────────────────────────────┐
    │             STAGING / SILVER ZONE            │
    │  - Normalized column names & data types      │
    │  - Deduped records, filtered deleted state   │
    │  - 1:1 row correspondence with source grain  │
    └──────────────────────┬───────────────────────┘
                           ▼
    ┌──────────────────────────────────────────────┐
    │         CORE DIMENSIONAL WAREHOUSE           │
    │  - Conformed Facts (events, transactions)    │
    │  - Conformed Dimensions (users, products)    │
    │  - Slowly Changing Dimension (SCD) history   │
    └──────────────────────┬───────────────────────┘
                           ▼
    ┌──────────────────────────────────────────────┐
    │              DATA MARTS / GOLD               │
    │  - Aggregated metrics, precomputed rollups   │
    │  - Tailored to specific domains (Sales, Ads) │
    │  - Directly queried by BI dashboards and ML  │
    └──────────────────────────────────────────────┘
```

---

## 3. Row-Oriented vs Columnar Storage Physics

### Row-Oriented (OLTP: PostgreSQL, MySQL, CSV)
- Data is written contiguously row-by-row on disk pages:
  `[Row 1: ID, Name, Age, Address, Bio, Balance] [Row 2: ID, Name, Age, Address, Bio, Balance]`
- **Superpower**: Extremely fast single-record writes (`INSERT INTO`) and point lookups (`SELECT * WHERE id = 42`).
- **Fatal Flaw for Analytics**: When querying `SELECT SUM(balance) FROM users`, the disk head and OS cache must read the entire page—including `Name`, `Address`, and `Bio`—wasting 95% of disk I/O bandwidth.

### Columnar Storage (OLAP: Parquet, DuckDB, Snowflake)
- Data is organized contiguously column-by-column in row groups:
  `[Col ID: 1, 2, 3...] [Col Name: Alice, Bob...] [Col Balance: 100, 250, 400...]`
- **Superpower**:
  1. **Column Pruning**: If a query touches only `balance`, zero bytes are read from disk for the remaining 50 columns.
  2. **High Compression**: Similar data types grouped together compress dramatically better (Snappy, ZSTD, Dictionary encoding).
  3. **Vectorized SIMD Processing**: Modern CPU registers process hundreds of numbers in parallel.

---

## 4. Orchestration: Dependency Graph (DAG) vs Chronological Clock

```text
Naive Thinking:
"Run Step A at 02:00, Step B at 02:30, Step C at 03:00"
(Breaks immediately when Step A takes 35 minutes due to network slowdown!)

Data Engineering Mental Model:
Step B depends strictly on Step A completing successfully.
Step C depends on Step A completing successfully.
Step D depends on both Step B and Step C.
```

- Orchestration is **topological ordering of a Directed Acyclic Graph (DAG)**, not a naive cron schedule.
- A schedule triggers the entrypoint of the DAG, but execution flow is governed by task state transitions:
  `PENDING` -> `RUNNING` -> `SUCCESS` -> (triggers downstream) or `FAILED` -> (skips downstream and alerts).

---

## 5. Event Time vs Processing Time vs Ingestion Time

```text
   10:00:00                 10:05:00                10:15:00
┌──────────────┐         ┌──────────────┐        ┌──────────────┐
│  EVENT TIME  │         │INGESTION TIME│        │PROCESSING TIME│
│ Phone clicks │ ──────> │ Arrives at   │ ─────> │ Worker runs  │
│ in subway    │ (lag)   │ Kafka Broker │ (lag)  │ Aggregation  │
└──────────────┘         └──────────────┘        └──────────────┘
```

- **Event Time**: The physical wall-clock instant the user clicked or the sensor fired on the device.
- **Ingestion Time**: The timestamp recorded when the broker or object store accepted the message.
- **Processing Time**: The local machine clock when the worker node processes the record.
- **Invariant**: Business metrics (daily active users, hourly revenue) must **always** be calculated over **Event Time**. Calculating over processing time makes metrics dependent on network latency and pipeline downtime.

---

## 6. The Lakehouse Mental Model: Files + Metadata = Tables

In traditional databases, tables and files are deeply entangled in proprietary binary engines.
In modern lakehouses (Apache Iceberg, Delta Lake):
```text
Table Abstraction
   │
   ├── Snapshot Pointer (Current active version)
   │     │
   │     ▼
   ├── Manifest List (Metadata tree tracking partition statistics & min/max bounds)
   │     │
   │     ▼
   └── Data Files (Immutable Apache Parquet files stored in cheap object storage)
```
- A lakehouse table is not a physical directory. It is a **metadata tree** pointing to immutable Parquet data files.
- Writes are ACID because they write new Parquet files and commit a new snapshot pointer atomically. Readers always see a consistent, isolated snapshot without locking writers.
