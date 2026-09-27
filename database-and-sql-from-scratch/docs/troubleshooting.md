# Database & SQL Troubleshooting Guide

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. The Five Classic SQL Query Bugs

### Bug 1: The `NOT IN (subquery)` NULL Black Hole
- **Symptom:** Query returns 0 rows when you know thousands of matching records exist.
- **Root Cause:** If the subquery evaluates to even a single `NULL`, `x NOT IN (1, 2, NULL)` evaluates to `UNKNOWN` for all rows. SQL's `WHERE` clause drops anything that is not `TRUE`.
- **Fix:** Use `NOT EXISTS`:
  ```sql
  -- BROKEN:
  SELECT * FROM customers WHERE id NOT IN (SELECT customer_id FROM orders);

  -- CORRECT:
  SELECT * FROM customers c 
  WHERE NOT EXISTS (
      SELECT 1 FROM orders o WHERE o.customer_id = c.id
  );
  ```

### Bug 2: Cardinality Explosion via Multiple 1:N Joins
- **Symptom:** `SUM(amount)` or `COUNT(*)` returns numbers that are 3x to 10x larger than reality.
- **Root Cause:** Joining `orders` (1:N) and `refunds` (1:N) to `customers` in a single query creates an $N \times M$ Cartesian product of order items and refund items.
- **Fix:** Aggregate before joining using CTEs or subqueries so the join occurs at a 1:1 grain.

### Bug 3: Accidental Inner Join on Left Join Chain
- **Symptom:** Unmatched left rows disappear despite using `LEFT JOIN`.
- **Root Cause:** Placing a right-table predicate in the `WHERE` clause:
  ```sql
  -- BROKEN: turns into an INNER JOIN because NULL = 'paid' is FALSE
  SELECT c.name, o.total_amount
  FROM customers c
  LEFT JOIN orders o ON c.id = o.customer_id
  WHERE o.status = 'paid';

  -- CORRECT: put predicate in the JOIN condition
  SELECT c.name, o.total_amount
  FROM customers c
  LEFT JOIN orders o 
      ON c.id = o.customer_id 
     AND o.status = 'paid';
  ```

### Bug 4: Non-Deterministic Pagination Slicing
- **Symptom:** Users see duplicate items across page 1 and page 2, or miss items entirely.
- **Root Cause:** `ORDER BY created_at LIMIT 10 OFFSET 10` where multiple rows share the same `created_at` timestamp. Without a tie-breaker, the engine is free to reorder them arbitrarily.
- **Fix:** Always append a unique column to your sort: `ORDER BY created_at DESC, id ASC`.

### Bug 5: Index Invalidation via Expression Wrapping
- **Symptom:** An indexed column suddenly triggers a 10-second Sequential Scan.
- **Root Cause:** Wrapping the indexed column in a function in the `WHERE` clause:
  ```sql
  -- BROKEN: invalidates standard B-Tree index on created_at
  WHERE DATE(created_at) = '2026-03-01';

  -- CORRECT: use sargable range comparison
  WHERE created_at >= '2026-03-01' AND created_at < '2026-03-02';
  ```

---

## 2. Concurrency & Performance Troubleshooting

| Issue | Diagnostic Command | Remediation |
| :--- | :--- | :--- |
| **Deadlock Detected** | Inspect server log for `deadlock detected` details | Ensure all transactions acquire locks in the identical deterministic order (e.g. order IDs sorted ascending). |
| **Long-Running Lock Contention** | `SELECT * FROM pg_locks WHERE NOT granted;` | Identify blocking PID with `pg_blocking_pids()` and terminate with `pg_cancel_backend()`. |
| **Work_mem Disk Spill** | Check `EXPLAIN ANALYZE` for `Sort Method: external merge Disk` | Increase `work_mem` for the query session: `SET work_mem = '64MB';` |
| **Bloated Table / Dead Tuples** | `SELECT n_dead_tup, n_live_tup FROM pg_stat_user_tables;` | Run `VACUUM (VERBOSE, ANALYZE) table_name;` to clean dead MVCC tuple versions. |
