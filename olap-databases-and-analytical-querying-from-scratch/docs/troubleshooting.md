# Analytical Database Troubleshooting Guide

A practical reference for diagnosing and resolving real-world failures across DuckDB, ClickHouse, Parquet lakes, and PostgreSQL comparison environments.

---

## 1. Out of Memory (OOM) During Queries

### Symptoms:
- ClickHouse: `Code: 241. DB::Exception: Memory limit (for query) exceeded: would use 10.20 GiB (limit: 10.00 GiB).`
- DuckDB: `Error: Out of Memory Error: could not allocate ...`
- Linux kernel: `OOM killer terminated process`.

### Root Causes:
1. **Unbounded High-Cardinality GROUP BY**: Grouping on raw UUIDs, URLs, or free-text strings.
2. **Hash Join with Oversized Build Side**: Large fact table placed on the Build side of a hash join instead of the Probe side.
3. **Exact Distinct Count / Percentiles**: `COUNT(DISTINCT uuid)` or `PERCENTILE_CONT` across 100M+ rows.

### Immediate Diagnoses:
```sql
-- ClickHouse: Inspect memory usage of recent failing queries
SELECT
    query_id,
    query,
    formatReadableSize(memory_usage) AS peak_memory,
    elapsed,
    exception
FROM system.query_log
WHERE type = 'QueryFinish' OR type = 'ExceptionWhileProcessing'
ORDER BY event_time DESC
LIMIT 10;
```

### Remediation:
- Enable disk spilling:
  - In ClickHouse: `SET max_bytes_before_external_group_by = 2000000000;`
  - In DuckDB: `PRAGMA max_memory='4GB';` (DuckDB automatically spills to temporary directory `temp_directory`).
- Replace exact functions with sketches:
  - Replace `COUNT(DISTINCT x)` with `uniqHLL12(x)` or `approx_count_distinct(x)`.
  - Replace exact quantile with `quantileTiming` or `approx_quantile`.

---

## 2. ClickHouse: "Too Many Parts" (Merge Backlog)

### Symptoms:
- Client receives: `Code: 252. DB::Exception: Too many parts in all data parts in table (300). Merges are processing significantly slower than inserts.`
- All write queries are rejected with HTTP 500.

### Root Causes:
1. **Tiny Insert Anti-Pattern**: Client application sends single-row or micro-batch inserts (e.g. 10 rows every 50ms).
2. **Disk I/O Saturation**: Storage disk cannot keep up with merge throughput.
3. **Partition Explosion**: Inserting data with high-cardinality partition keys creates hundreds of parts per insert.

### Immediate Diagnoses:
```sql
-- Check active parts count per table
SELECT
    table,
    count() AS total_parts,
    sum(rows) AS total_rows,
    formatReadableSize(sum(bytes_on_disk)) AS disk_size
FROM system.parts
WHERE active = 1
GROUP BY table
ORDER BY total_parts DESC;

-- Inspect currently executing background merges
SELECT
    table,
    elapsed,
    progress,
    formatReadableSize(total_size_bytes_compressed) AS total_size,
    memory_usage
FROM system.merges;
```

### Remediation:
1. **Buffer Client Writes**: Aggregate inserts into batches of 20,000 to 100,000 rows before issuing `INSERT`.
2. **Enable ClickHouse Asynchronous Inserts**:
   ```sql
   SET async_insert = 1;
   SET wait_for_async_insert = 0;
   ```
3. **Optimize Partitions**: Ensure `PARTITION BY` groups coarsely (e.g. `toYYYYMM(event_time)` instead of daily or hourly).

---

## 3. Query Scans 100% of Data Despite Selective WHERE Clause

### Symptoms:
- Query latency is identical whether filtering for 1 day or 5 years of data.
- Profiler reports `RowsRead` equals total table row count.

### Root Causes:
1. **Expression Wrapped Around Column in WHERE**:
   - Bad: `WHERE toYear(created_at) = 2026`
   - Good: `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`
   Wrapping a partition or sort column in a non-deterministic or custom function prevents partition pruning and sparse index skipping.
2. **Filter Column Missing from Primary Sort Key**:
   Table is ordered by `(country, category)`, but query filters solely by `category = 'Electronics'`.

### Immediate Diagnoses:
```sql
-- DuckDB: Inspect physical plan operators and scanned columns
EXPLAIN ANALYZE SELECT ...;

-- ClickHouse: Inspect index analysis
EXPLAIN indexes = 1 SELECT ...;
```
Look for:
- `Selected Parts: X / Total Parts: Y`
- `Selected Marks: A / Total Marks: B`
- If Marks read equals total marks, your sort key was bypassed.

---

## 4. DuckDB: Database File Locked (`database is locked`)

### Symptoms:
- Exception: `duckdb.IOException: IO Error: Could not set lock on file ... Database is already open in another process.`

### Root Causes:
DuckDB is an in-process database. By default, only **one** process can hold a read-write lock on a database file. If another script, Jupyter notebook, or CLI terminal has `outputs/olap_lab.duckdb` open with write access, all other processes are blocked.

### Remediation:
1. Connect in **read-only mode** for concurrent query analysis:
   ```python
   con = duckdb.connect("outputs/olap_lab.duckdb", read_only=True)
   ```
2. Or query Parquet files directly without touching the `.duckdb` file:
   ```python
   con = duckdb.connect() # in-memory connection
   con.execute("SELECT * FROM read_parquet('datasets/ecommerce/*.parquet')")
   ```
3. Identify and terminate rogue locking processes:
   ```bash
   lsof | grep olap_lab.duckdb
   ```
