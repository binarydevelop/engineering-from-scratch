# Analytical Query Drill: DRILL-COHO-02

## Drill Metadata
- **Category**: `cohorts`
- **Drill ID**: `DRILL-COHO-02`
- **Difficulty**: Foundational
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
User Acquisition Cohort Drill #2: Query source `dim_users JOIN fact_order_items` grouping by `signup_date, created_at` to compute `COUNT(DISTINCT user_id)`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `dim_users JOIN fact_order_items`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
