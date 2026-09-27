# Analytical Query Drill: DRILL-AGGR-14

## Drill Metadata
- **Category**: `aggregation`
- **Drill ID**: `DRILL-AGGR-14`
- **Difficulty**: Advanced
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
Fact Aggregation Drill #14: Query source `fact_order_items` grouping by `category, country` to compute `SUM(net_revenue), COUNT(*)`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `fact_order_items`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
