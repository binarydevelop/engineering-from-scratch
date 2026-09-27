# Phase 03: Sql Query Anatomy

> **Motto:** SQL says WHAT result is needed; the database decides HOW to obtain it.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 02  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **SQL says WHAT result is needed; the database decides HOW to obtain it.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Treating SQL like imperative Python leads to inefficient procedural loops instead of leveraging set-based relational operators.

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

Declarative programming: the query is a formal specification of the desired mathematical relation.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
SQL Query (WHAT) ──► Query Optimizer ──► Execution Plan (HOW) ──► Results
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT first_name, last_name FROM ecommerce.customers WHERE status = 'active' ORDER BY last_name ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT first_name, last_name FROM ecommerce.customers WHERE status = 'active' ORDER BY last_name ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT first_name, last_name FROM ecommerce.customers WHERE status = 'active' ORDER BY last_name ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT first_name FROM ecommerce.customers WHERE unknown_col = 1; -- Semantic validation error
```

---

## 10. Debug It & Fix It

Check catalog pg_attribute during parse analysis.

---

## 11. Evidence Ledger

```text
Lesson: Phase 03 — Sql Query Anatomy
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: SQL says WHAT result is needed; the database decides HOW to obtain it.
```

---

## 12. Exercises

Level 1: Identify SELECT and FROM clauses.
Level 5: Trace the transformation of AST to Query Tree.
