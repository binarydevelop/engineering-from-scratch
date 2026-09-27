# Broken OLAP Lab: lab-08-cartesian-join-explosion

## Scenario & Incident Report: Accidental Cartesian Join Explosion
- **Category**: `joins`
- **System**: ClickHouse / DuckDB / Parquet Engine
- **Severity**: High (Production SLA Breach)

---

## 1. The Incident
A query joins two fact tables on an incomplete key, creating an accidental many-to-many join explosion that generates 100 million intermediate rows.

## 2. Broken Implementation / Query
```sql
SELECT count(*) FROM fact_order_items a JOIN fact_order_items b ON a.country = b.country;
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
*Do not consult `solutions/broken-systems/lab-08-cartesian-join-explosion_solution.md` until you have diagnosed the root cause!*
