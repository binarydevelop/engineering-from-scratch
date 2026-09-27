# Phase 05: Where Deeply

> **Motto:** Filter early, filter aggressively; every discarded tuple saves downstream CPU and RAM.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 04  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Filter early, filter aggressively; every discarded tuple saves downstream CPU and RAM.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Misunderstanding boolean operator precedence (AND has higher precedence than OR) causes severe security leaks and data corruption.

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

Relational Selection (σ): extracts tuples that satisfy a propositional predicate.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Rows (N) ──► [ Predicate σ(P) ] ──► Surviving Rows (M <= N)
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT * FROM ecommerce.products WHERE (category_id = 2 OR category_id = 3) AND price < 500.00;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT * FROM ecommerce.products WHERE (category_id = 2 OR category_id = 3) AND price < 500.00;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT * FROM ecommerce.products WHERE (category_id = 2 OR category_id = 3) AND price < 500.00;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT * FROM ecommerce.products WHERE category_id = 2 OR category_id = 3 AND price < 500.00; -- Operator precedence bug!
```

---

## 10. Debug It & Fix It

Parenthesize compound boolean expressions explicitly.

---

## 11. Evidence Ledger

```text
Lesson: Phase 05 — Where Deeply
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Filter early, filter aggressively; every discarded tuple saves downstream CPU and RAM.
```

---

## 12. Exercises

Level 1: Filter on equality.
Level 5: Analyze index sargability of complex WHERE clauses.
