# Analytical Query Drill: DRILL-OPTI-06

## Drill Metadata
- **Category**: `optimization`
- **Drill ID**: `DRILL-OPTI-06`
- **Difficulty**: Intermediate
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
Zone Map & Pushdown Optimization Drill #6: Query source `sensor_readings` grouping by `device_id, timestamp` to compute `Filter on sorted timestamp prefix`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `sensor_readings`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
