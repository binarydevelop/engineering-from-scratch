# Analytical Query Drill: DRILL-RETE-03

## Drill Metadata
- **Category**: `retention`
- **Drill ID**: `DRILL-RETE-03`
- **Difficulty**: Foundational
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
N-Day Activity Retention Drill #3: Query source `web_events` grouping by `user_id, event_time` to compute `COUNT(DISTINCT user_id) active on Day N`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `web_events`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
