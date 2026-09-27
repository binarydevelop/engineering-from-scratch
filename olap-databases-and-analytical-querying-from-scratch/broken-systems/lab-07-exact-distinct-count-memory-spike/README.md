# Broken OLAP Lab: lab-07-exact-distinct-count-memory-spike

## Scenario & Incident Report: Exact COUNT(DISTINCT) Memory Saturation
- **Category**: `aggregations`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Executive dashboard runs COUNT(DISTINCT user_id) over 1 billion rows, consuming 32 GB RAM.

## 2. Broken Implementation / Query
```sql
SELECT count(DISTINCT user_id) FROM web_events;
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
*Do not consult `solutions/broken-systems/lab-07-exact-distinct-count-memory-spike_solution.md` until you have diagnosed the root cause!*
