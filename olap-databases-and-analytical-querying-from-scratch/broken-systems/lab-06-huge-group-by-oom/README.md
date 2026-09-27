# Broken OLAP Lab: lab-06-huge-group-by-oom

## Scenario & Incident Report: Out-Of-Memory from High-Cardinality GROUP BY
- **Category**: `memory`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Query groups by an unconstrained UUID across 50 million rows, blowing past available query memory limits.

## 2. Broken Implementation / Query
```sql
SELECT request_uuid, count(*) FROM service_logs GROUP BY request_uuid;
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
*Do not consult `solutions/broken-systems/lab-06-huge-group-by-oom_solution.md` until you have diagnosed the root cause!*
