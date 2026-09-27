# Broken OLAP Lab: lab-02-unpartitioned-date-scan

## Scenario & Incident Report: Full Table Scan from Unpruned Date Predicate
- **Category**: `partitioning`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Query filters by wrapping a column in a function (e.g. toYear(created_at) = 2025), preventing partition pruning and forcing a full scan of 5 years of historical data.

## 2. Broken Implementation / Query
```sql
SELECT count(*) FROM fact_order_items WHERE extract(year from created_at) = 2025;
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
*Do not consult `solutions/broken-systems/lab-02-unpartitioned-date-scan_solution.md` until you have diagnosed the root cause!*
