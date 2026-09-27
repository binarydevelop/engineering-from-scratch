# Broken OLAP Lab: lab-01-select-star-io-explosion

## Scenario & Incident Report: SELECT * Columnar I/O Explosion
- **Category**: `query-plan`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
A dashboard query issues SELECT * against a 60-column fact table across 10 million rows, causing severe NVMe I/O saturation and 8-second query latency.

## 2. Broken Implementation / Query
```sql
SELECT * FROM fact_order_items WHERE created_at >= '2025-01-01';
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
*Do not consult `solutions/broken-systems/lab-01-select-star-io-explosion_solution.md` until you have diagnosed the root cause!*
