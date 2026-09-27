# Broken OLAP Lab: lab-09-hash-join-build-side-blowup

## Scenario & Incident Report: Oversized Build Side in Distributed Hash Join
- **Category**: `joins`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Query planner puts a 50 GB fact table on the Build side and a 10 MB dimension table on the Probe side.

## 2. Broken Implementation / Query
```sql
SELECT * FROM large_fact JOIN small_dim ON large_fact.dim_id = small_dim.id;
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
*Do not consult `solutions/broken-systems/lab-09-hash-join-build-side-blowup_solution.md` until you have diagnosed the root cause!*
