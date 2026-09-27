# Phase 13: Data Modification

> **Motto:** Every INSERT, UPDATE, and DELETE is a transaction that generates WAL and affects MVCC tuple versions.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 12  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Every INSERT, UPDATE, and DELETE is a transaction that generates WAL and affects MVCC tuple versions.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

An accidental UPDATE or DELETE without a WHERE clause can wipe an entire production database in milliseconds.

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

PostgreSQL Append-Only MVCC: UPDATE writes a new tuple version and sets xmax on the old tuple.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Old Tuple: (xmin=100, xmax=102) [Dead]
New Tuple: (xmin=102, xmax=0)   [Live]
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
INSERT INTO ecommerce.customers (email, first_name, last_name) VALUES ('new@ex.com', 'New', 'User') RETURNING id, created_at;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "INSERT INTO ecommerce.customers (email, first_name, last_name) VALUES ('new@ex.com', 'New', 'User') RETURNING id, created_at;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
INSERT INTO ecommerce.customers (email, first_name, last_name) VALUES ('new@ex.com', 'New', 'User') RETURNING id, created_at;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
UPDATE ecommerce.customers SET status = 'active'; -- Catastrophe: missing WHERE clause!
```

---

## 10. Debug It & Fix It

Always test updates inside a transaction: BEGIN; UPDATE ...; ROLLBACK;

---

## 11. Evidence Ledger

```text
Lesson: Phase 13 — Data Modification
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Every INSERT, UPDATE, and DELETE is a transaction that generates WAL and affects MVCC tuple versions.
```

---

## 12. Exercises

Level 1: Safe insert.
Level 5: Inspect xmin/xmax tuple headers in page inspection after update.
