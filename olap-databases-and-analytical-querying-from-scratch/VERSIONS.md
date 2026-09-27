# Technology Stack and Version Discipline

To guarantee reproducibility across local, containerized, and benchmarking environments, every technology used in **OLAP Databases and Analytical Querying from Scratch** is pinned to a specific stable release.

---

## 1. Pinned Primary Systems & Engines

| System | Role in Course | Version | Packaging / Distribution | Notes & Architectural Invariants |
| :--- | :--- | :--- | :--- | :--- |
| **DuckDB** | In-Process Vectorized OLAP | `1.5.5` | Native Python Wheel / Binary | Vector size 2048, Pushdown optimizations, Arrow IPC integration, Parquet scanner |
| **ClickHouse** | Primary Production Columnar DBMS | `24.8-alpine` | Official Docker Image (`clickhouse/clickhouse-server:24.8-alpine`) | MergeTree engine family, immutable parts, primary/sorting sparse indexing, mark cache, vectorized SIMD aggregations |
| **PostgreSQL** | OLTP Baseline Comparison | `16.4-alpine` | Official Docker Image (`postgres:16.4-alpine`) | Heap-based row store, MVCC, B-tree indexes, tuple-at-a-time volcano iterator |
| **Apache Druid** | Event-Oriented Stream OLAP | `30.0.0` | Official Container / Specification Reference | Time-chunked immutable segments, bitmap indexing, ingestion rollup, broker fan-out |
| **Apache Pinot** | Real-Time Analytical Serving | `1.2.0` | Official Container / Specification Reference | Realtime / Offline segment pairs, star-tree index, sorted inverted indexes |
| **PyArrow** | Columnar Memory & File Layout | `25.0.1` | Python Wheel | Apache Arrow IPC, Parquet metadata reader/writer, dictionary encoding |
| **Python** | Simulation Harness & Test Suite | `3.11+` | macOS/Linux ARM64 / x86_64 | Educational engines, simulation models, statistical assertions |

---

## 2. Python Client Libraries & Drivers

| Library | Version | Purpose |
| :--- | :--- | :--- |
| `clickhouse-connect` | `1.9.0` | Native HTTP/Arrow client for ClickHouse communication |
| `psycopg2-binary` | `2.9.13` | PostgreSQL binary adapter for comparative benchmark harness |
| `lz4` | `4.4.5` | Fast compression / decompression benchmarking |
| `rich` | `15.0.0` | Terminal query plan visualization and metrics output formatting |
| `tabulate` | `0.10.0` | Tabular query results and storage comparisons |
| `sqlparse` | `0.6.0` | SQL formatting and AST parsing experiments |
| `pytest` | `9.1.1` | Automated test suite for analytical correctness and query verification |

---

## 3. SQL Dialect & Concept Classification

In this course, we strictly categorize every query and DDL statement into three distinct tiers:

### Tier 1: ANSI / Standard SQL Concepts
Concepts portable across all analytical and relational engines:
- Standard projection (`SELECT col1, col2`)
- Predicate evaluation (`WHERE col >= val AND col2 IN (...)`)
- Grouping & aggregations (`GROUP BY`, `HAVING`, `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`)
- Standard Joins (`INNER JOIN`, `LEFT JOIN`, `FULL OUTER JOIN`)
- Standard Window Functions (`ROW_NUMBER() OVER (...)`, `LAG()`, `LEAD()`, `RANK()`, `SUM() OVER (...)`)
- Common Table Expressions (`WITH ... AS (...)`)

### Tier 2: Analytical & Columnar Concepts
Architectural primitives implemented differently across engines:
- Quantiles & Percentiles (`quantileExact`, `approx_quantile`, `percentile_cont`)
- Approximate distinct counting (`approx_count_distinct`, `uniqHLL12`, `HyperLogLog`)
- Time bucketing (`date_trunc`, `toStartOfInterval`, `TIME_FLOOR`)
- Array / Nested transformations (`UNNEST`, `arrayJoin`)
- Bitwise aggregation & bitmaps

### Tier 3: Database-Specific Syntax & Engines
Physical directives that are engine-proprietary:
- **ClickHouse**:
  - `ENGINE = MergeTree()`
  - `PARTITION BY toYYYYMM(timestamp)`
  - `ORDER BY (tenant_id, timestamp, event_id)`
  - `SETTINGS index_granularity = 8192`
  - `quantileExact(0.95)(latency)`
  - `uniqExact(user_id)` vs `uniq(user_id)`
  - Materialized views with `TO target_table`
  - Projections: `ALTER TABLE ... ADD PROJECTION ...`
- **DuckDB**:
  - Direct Parquet scan: `SELECT * FROM read_parquet('data/*.parquet')`
  - In-memory data chunk inspection: `EXPLAIN ANALYZE`
  - Struct & list builders: `{'a': 1, 'b': [1, 2, 3]}`
- **PostgreSQL**:
  - `EXPLAIN (ANALYZE, BUFFERS, SETTINGS)`
  - `CREATE INDEX ... USING btree (...)`
  - `PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency)`

---

## 4. Storage Engine & API Deprecation Policy

To prevent learners from absorbing obsolete industry practices:
1. **Never use deprecated ClickHouse engines**: We do not use legacy `Log`, `TinyLog`, or deprecated `Distributed` table syntax without proper cluster configuration.
2. **Never teach raw tuple-by-tuple UDFs without vectorization awareness**: We highlight why row-by-row scalar functions kill vector performance.
3. **No unpinned `latest` container tags**: All Docker images must declare exact major.minor tags.
4. **Transparent benchmark reporting**: No benchmark is valid unless the exact CPU model, RAM size, disk type (NVMe/SSD), engine version, cache state (cold vs warm), and row count are logged in the benchmark artifact.
