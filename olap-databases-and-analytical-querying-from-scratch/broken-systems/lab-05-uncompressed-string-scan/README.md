# Broken OLAP Lab: lab-05-uncompressed-string-scan

## Scenario & Incident Report: Uncompressed High-Cardinality String Scan
- **Category**: `compression`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
Country and URL columns are stored as raw uncompressed strings instead of LowCardinality / dictionary encoding, inflating disk footprint by 4x.

## 2. Broken Implementation / Query
```sql
ALTER TABLE events ADD COLUMN country String;
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
*Do not consult `solutions/broken-systems/lab-05-uncompressed-string-scan_solution.md` until you have diagnosed the root cause!*
