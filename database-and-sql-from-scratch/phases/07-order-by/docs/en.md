# Phase 07: Order By

> **Motto:** A relational table is an unordered set; without ORDER BY, row ordering is completely undefined.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 06  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **A relational table is an unordered set; without ORDER BY, row ordering is completely undefined.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Relying on implicit insertion order or index order causes subtle, non-reproducible pagination bugs in production.

When engineers operate on blind assumptions, queries return incorrect grain, Cartesian duplicates slip into reports, and database CPU saturates under unexpected sequential scans.

---

## 3. Predict

Before executing any queries in this phase:
- What should one output row represent (Grain)?
- How many rows do you predict will be returned?
- Will the planner choose an Index Scan, Bitmap Heap Scan, or Sequential Scan?
- How will the query handle edge cases and NULL values?

---

## 4. First Principles & Relational Algebra

Relational tables are unordered bags of tuples. The engine may read them in any physical order (parallel scans, bitmap scans, sequential sweeps).

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Unordered Tuples ──► [ Sort Operator / B-Tree Index ] ──► Ordered Output Sequence
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, total_amount, order_date FROM ecommerce.orders ORDER BY total_amount DESC, id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, total_amount, order_date FROM ecommerce.orders ORDER BY total_amount DESC, id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, total_amount, order_date FROM ecommerce.orders ORDER BY total_amount DESC, id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT id FROM ecommerce.orders ORDER BY order_date; -- Non-deterministic if identical dates exist!
```

---

## 10. Debug It & Fix It

Always provide an unambiguous primary key tie-breaker.

---

## 11. Evidence Ledger

```text
Lesson: Phase 07 — Order By
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: A relational table is an unordered set; without ORDER BY, row ordering is completely undefined.
```

---

## 12. Exercises

Level 1: Sort by one column.
Level 5: Check EXPLAIN for external merge disk spills vs quicksort.
