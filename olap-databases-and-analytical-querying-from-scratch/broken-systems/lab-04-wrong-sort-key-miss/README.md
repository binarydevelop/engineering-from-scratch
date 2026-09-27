# Broken OLAP Lab: lab-04-wrong-sort-key-miss

## Scenario & Incident Report: Sort Key Miss Leading to 100% Block Scan
- **Category**: `sorting`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Table is sorted by (event_id), but 99% of queries filter by (tenant_id, timestamp), rendering sparse primary indexes and zone maps ineffective.

## 2. Broken Implementation / Query
```sql
SELECT sum(revenue) FROM events WHERE tenant_id = 42 AND timestamp >= '2025-06-01';
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
*Do not consult `solutions/broken-systems/lab-04-wrong-sort-key-miss_solution.md` until you have diagnosed the root cause!*
