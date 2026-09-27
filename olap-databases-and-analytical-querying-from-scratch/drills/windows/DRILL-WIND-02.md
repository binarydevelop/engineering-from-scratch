# Analytical Query Drill: DRILL-WIND-02

## Drill Metadata
- **Category**: `windows`
- **Drill ID**: `DRILL-WIND-02`
- **Difficulty**: Foundational
- **Dialect**: `DuckDB / ANSI SQL`

---

## 1. Problem Statement
Window Frame & Partition Drill #2: Query source `web_events` grouping by `user_id, event_time` to compute `ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_time)`.

## 2. Invariant Checklist
Before writing your query, confirm:
- [ ] What is the exact input row grain of `web_events`?
- [ ] What is the expected output grain of this drill?
- [ ] Which columns can be safely omitted from the scan?
- [ ] Can partition pruning or data skipping eliminate unneeded blocks?

## 3. Drill Assignment
Formulate the query. Inspect its physical plan using `EXPLAIN ANALYZE`.
Verify that your query does NOT perform full row scans or unbounded hash joins.
