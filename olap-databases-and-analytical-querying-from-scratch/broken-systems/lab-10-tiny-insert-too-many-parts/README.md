# Broken OLAP Lab: lab-10-tiny-insert-too-many-parts

## Scenario & Incident Report: ClickHouse Too Many Parts Write Rejection
- **Category**: `ingestion`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Micro-service sends 100 single-row inserts per second to ClickHouse, triggering 'Too many parts in all data parts in table (300)'.

## 2. Broken Implementation / Query
```sql
for row in stream: client.insert('INSERT INTO events VALUES (...)')
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
*Do not consult `solutions/broken-systems/lab-10-tiny-insert-too-many-parts_solution.md` until you have diagnosed the root cause!*
