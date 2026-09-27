# Broken OLAP Lab: lab-03-high-cardinality-partition-explosion

## Scenario & Incident Report: Million-Partition Inode and Metadata Exhaustion
- **Category**: `partitioning`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Table is partitioned by user_id, creating 100,000 tiny parts and exhausting OS file handles during ingestion.

## 2. Broken Implementation / Query
```sql
CREATE TABLE events (user_id UInt64, ...) ENGINE = MergeTree() PARTITION BY user_id ORDER BY timestamp;
```

## 3. Reproduction & Investigation Steps
1. Run the broken query using the benchmark runner:
   ```bash
   .venv/bin/python scripts/benchmark.py --suite broken
   ```
2. Inspect the query plan via `EXPLAIN ANALYZE` or `system.query_log`.
3. Answer:
   - How many rows were scanned vs required?
   - How many bytes were pulled from disk?
   - Which physical operator consumed peak CPU or memory?

## 4. Your Challenge
Diagnose the exact physical failure mechanism and formulate the architectural fix.
*Do not consult `solutions/broken-systems/lab-03-high-cardinality-partition-explosion_solution.md` until you have diagnosed the root cause!*
