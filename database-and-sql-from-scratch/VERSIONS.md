# Pinned Software & Specification Versions

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

This document establishes the official software versions, engine specifications, and compatibility boundaries used throughout `database-and-sql-from-scratch`. To ensure reproducibility across local machines, continuous integration, and container environments, all examples, benchmarks, query plans, and exercises are pinned and verified against these versions.

---

## 1. Pinned Primary Engine

| Component | Pinned Version | Image / Distribution | Purpose |
| :--- | :--- | :--- | :--- |
| **PostgreSQL** | **16.4** (Major: 16 LTS) | `postgres:16.4-alpine` | Primary RDBMS engine for all exercises, plans, MVCC, and benchmarks |
| **psql CLI** | **16.x** or higher | Client binary | Interactive query terminal, metadata inspection (`\d`, `\ef`, `\x`) |
| **Python** | **3.11+** | CPython | Query grader, mini-RDBMS engine, database application labs |
| **Docker Compose** | **v2.20+** | Docker Desktop / Engine | Reproducible isolated database provisioning |

---

## 2. Why PostgreSQL 16?

PostgreSQL 16 was selected as our stable reference version for several critical architectural reasons:

1. **Long-Term Enterprise Stability:** PostgreSQL 16 is an active LTS release supported through November 2028 with widespread production deployment across AWS RDS/Aurora, Google Cloud SQL, and Azure Database.
2. **Advanced Planner & Executor Capabilities:**
   - Incremental sort optimizations.
   - Enhanced parallel hash joins and parallel aggregates.
   - Real-time I/O statistics monitoring via `pg_stat_io`.
   - Optimized `jsonb` subscripting and functions conforming to SQL:2016 / SQL:2023.
3. **Bi-Directional Logical Replication & Bidirectional Failover:** Provides clear, robust primitives for studying replication topologies and WAL streaming.
4. **Predictable Plan Costing:** Default cost parameters (`seq_page_cost = 1.0`, `random_page_cost = 4.0`, `cpu_tuple_cost = 0.01`) provide dependable, deterministic plans for all query analysis exercises.

---

## 3. The Three Critical Architectural Distinctions

A foundational flaw in superficial SQL courses is conflating language syntax with database engine behavior. In this curriculum, every concept is explicitly categorized into one of three domains:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Standard SQL Concept (ANSI/ISO SQL:92, SQL:1999, SQL:2016)         │
│    Portable across PostgreSQL, MySQL, Oracle, SQL Server, DuckDB, etc. │
│    Examples: SELECT, WHERE, JOIN, GROUP BY, HAVING, Subqueries, CTEs,  │
│    WINDOW functions (OVER, PARTITION BY, ORDER BY, ROWS BETWEEN).      │
├────────────────────────────────────────────────────────────────────────┤
│ 2. PostgreSQL-Specific SQL Syntax & Extensions                         │
│    Language extensions provided by Postgres for developer ergonomics.  │
│    Examples: ILIKE, ON CONFLICT DO UPDATE (Upsert), RETURNING,         │
│    DISTINCT ON (expr), generate_series(), JSONB operators (->, ->>, @>).│
├────────────────────────────────────────────────────────────────────────┤
│ 3. PostgreSQL Implementation Detail & Engine Internals                 │
│    Physical mechanics of the engine; not guaranteed across other DBMS. │
│    Examples: 8KB buffer pool pages, MVCC tuple headers (xmin/xmax),    │
│    TOAST out-of-line storage, WAL records, VACUUM / Autovacuum freeze, │
│    B-Tree Lehman & Yao concurrency, work_mem sort spill to disk.       │
└────────────────────────────────────────────────────────────────────────┘
```

When writing SQL in lessons:
- **Phases 00–48 (Foundational & Intermediate SQL):** We prioritize **Standard SQL** syntax so your query skills transfer seamlessly to SQLite, Snowflake, BigQuery, MySQL, or DuckDB.
- **Phases 49–74 (Relational Engineering & Query Internals):** We inspect the **PostgreSQL Implementation Details** through `EXPLAIN ANALYZE`, buffer cache inspection, and transaction isolation tests.
- **Phases 75–101 (Production & Advanced Applications):** We leverage **PostgreSQL-Specific Extensions** (JSONB, Upserts, Materialized Views, Keyset cursors) to demonstrate production-grade system engineering.

---

## 4. Verification Baseline Settings

The following PostgreSQL configuration parameters (`postgresql.conf`) are pinned in our Docker container to ensure identical execution plan output across all learner environments:

```ini
# Memory Configuration for Predictable Labs
shared_buffers = 128MB
work_mem = 4MB
maintenance_work_mem = 64MB
effective_cache_size = 512MB

# Query Planner Cost Parameters
seq_page_cost = 1.0
random_page_cost = 4.0
cpu_tuple_cost = 0.01
cpu_index_tuple_cost = 0.005
cpu_operator_cost = 0.0025

# Parallel Query (Configured for deterministic lab runs)
max_parallel_workers_per_gather = 2

# Logging & Monitoring
track_io_timing = on
track_functions = all
```

---

## 5. Client & Library Specifications

- **Python Database Driver:** `psycopg` v3.1+ (Python 3 DB-API 2.0 compliant with native binary protocol support and connection pool).
- **FastAPI / REST API:** v0.110+ for building the production application service in Phase 99.
- **Query Grader:** Custom zero-dependency CLI verification harness with `tabulate` output formatting.
