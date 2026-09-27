# Phase 06: Null And Three Valued Logic

> **Motto:** NULL is not zero, not empty string, and not equal to itself; it is the absence of known truth.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 05  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **NULL is not zero, not empty string, and not equal to itself; it is the absence of known truth.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Using col = NULL silently drops all rows. Using NOT IN with a subquery containing NULL drops the entire result set.

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

Kleene's 3-valued logic truth tables for AND, OR, and NOT when evaluated against UNKNOWN.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
NULL = NULL ──► UNKNOWN (Not TRUE!)
WHERE UNKNOWN ──► Dropped (WHERE requires TRUE to emit row)
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, email, COALESCE(bio, 'N/A') FROM social.users WHERE bio IS NULL;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, email, COALESCE(bio, 'N/A') FROM social.users WHERE bio IS NULL;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, email, COALESCE(bio, 'N/A') FROM social.users WHERE bio IS NULL;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT * FROM social.users WHERE bio = NULL; -- Returns 0 rows!
```

---

## 10. Debug It & Fix It

Use IS NULL and IS NOT NULL, never equality with NULL.

---

## 11. Evidence Ledger

```text
Lesson: Phase 06 — Null And Three Valued Logic
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: NULL is not zero, not empty string, and not equal to itself; it is the absence of known truth.
```

---

## 12. Exercises

Level 1: Filter on IS NULL.
Level 5: Trace truth table for NOT (UNKNOWN OR FALSE).
