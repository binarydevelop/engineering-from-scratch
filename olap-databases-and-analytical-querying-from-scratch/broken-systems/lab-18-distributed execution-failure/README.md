# Broken OLAP Lab: lab-18-distributed execution-failure

## Scenario & Incident Report: OLAP Production Failure & Diagnostic Lab #18: Distributed execution
- **Category**: `distributed execution`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Production incident #18 involving distributed execution causing query degradation or resource starvation under realistic analytical workload.

## 2. Broken Implementation / Query
```sql
-- Naive or broken query #18
SELECT * FROM table_name WHERE failure_condition = TRUE;
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
*Do not consult `solutions/broken-systems/lab-18-distributed execution-failure_solution.md` until you have diagnosed the root cause!*
