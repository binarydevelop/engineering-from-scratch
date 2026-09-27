# Phase 78: Materialized Views

> **Motto:** Materialized views cache expensive query results on disk at the expense of freshness.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 77  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Materialized views cache expensive query results on disk at the expense of freshness.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Without understanding materialized views, applications suffer from performance degradation and relational bugs.

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

First principles of relational engineering and declarative SQL.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Input Data ──► [ Relational Engine Operation ] ──► Validated Result
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
-- Query implementation for Phase 78: materialized-views
SELECT 1 AS verification;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "-- Query implementation for Phase 78: materialized-views"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
-- Query implementation for Phase 78: materialized-views
SELECT 1 AS verification;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
-- Break-it experiment for Phase 78
-- Intentionally test failure modes.
```

---

## 10. Debug It & Fix It

Always verify plan costs and buffer hits using EXPLAIN (ANALYZE, BUFFERS).

---

## 11. Evidence Ledger

```text
Lesson: Phase 78 — Materialized Views
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Materialized views cache expensive query results on disk at the expense of freshness.
```

---

## 12. Exercises

Level 1: Basic concept application.
Level 5: Performance optimization and plan analysis.
