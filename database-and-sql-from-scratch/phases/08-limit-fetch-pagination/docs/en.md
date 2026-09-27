# Phase 08: Limit Fetch Pagination

> **Motto:** Limit without deterministic ordering is random sampling in disguise.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 07  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Limit without deterministic ordering is random sampling in disguise.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

OFFSET 100,000 forces the engine to read and discard 100,000 rows, burning disk I/O and CPU.

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

Windowing over physical streams; resource bounds on query output buffers.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Engine Heap Scan (100,010 rows) ──► Discard 100,000 ──► Emit 10 rows (Brutal!)
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC LIMIT 5 OFFSET 0;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC LIMIT 5 OFFSET 0;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, name, price FROM ecommerce.products ORDER BY price DESC, id ASC LIMIT 5 OFFSET 0;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT * FROM ecommerce.products LIMIT 5; -- Non-deterministic across runs!
```

---

## 10. Debug It & Fix It

Use ORDER BY with unique key for reproducible slices.

---

## 11. Evidence Ledger

```text
Lesson: Phase 08 — Limit Fetch Pagination
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Limit without deterministic ordering is random sampling in disguise.
```

---

## 12. Exercises

Level 1: Slices top 5 rows.
Level 5: Measure latency scaling as OFFSET increases from 10 to 1,000,000.
