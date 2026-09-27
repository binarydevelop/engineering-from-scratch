# Phase 04: Select Deeply

> **Motto:** Every projected expression defines the attributes of your output relation.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 03  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Every projected expression defines the attributes of your output relation.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Lazy SELECT * leaks database internals, breaks application contracts when schemas evolve, and forces expensive heap scans instead of index-only scans.

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

Relational Projection (π): removes unwanted attributes and computes new derived values per tuple.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Table: [A, B, C, D] ──► π(A, B*2) ──► Result: [A, new_col]
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, first_name || ' ' || last_name AS full_name, created_at FROM ecommerce.customers ORDER BY id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, first_name || ' ' || last_name AS full_name, created_at FROM ecommerce.customers ORDER BY id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, first_name || ' ' || last_name AS full_name, created_at FROM ecommerce.customers ORDER BY id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT id, non_existent_col FROM ecommerce.customers; -- Compiler syntax error
```

---

## 10. Debug It & Fix It

Always project explicit columns needed by the consumer.

---

## 11. Evidence Ledger

```text
Lesson: Phase 04 — Select Deeply
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Every projected expression defines the attributes of your output relation.
```

---

## 12. Exercises

Level 1: Project 2 columns.
Level 5: Measure memory bandwidth impact of SELECT * vs projected columns.
