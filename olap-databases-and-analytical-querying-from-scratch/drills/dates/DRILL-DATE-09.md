# Analytical Query Drill: DRILL-DATE-09

## Drill Metadata
- **Category**: `dates`
- **Drill ID**: `DRILL-DATE-09`
- **Difficulty**: Intermediate
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
Date Truncation & Gap Fill Drill #9: Query source `service_logs` grouping by `date_trunc('hour', timestamp)` to compute `COUNT(*), AVG(latency_ms)`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `service_logs`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
