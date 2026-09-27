# Analytical Query Drill: DRILL-PERC-03

## Drill Metadata
- **Category**: `percentiles`
- **Drill ID**: `DRILL-PERC-03`
- **Difficulty**: Foundational
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
Latency Percentile & SLA Drill #3: Query source `service_logs` grouping by `endpoint` to compute `approx_quantile(latency_ms, 0.95)`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `service_logs`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
