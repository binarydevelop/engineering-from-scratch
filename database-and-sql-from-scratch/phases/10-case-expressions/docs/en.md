# Phase 10: Case Expressions

> **Motto:** CASE is an expression that returns a scalar value, not a procedural control-flow statement.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 09  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **CASE is an expression that returns a scalar value, not a procedural control-flow statement.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Novices try to use IF/ELSE in standard SQL, not realizing CASE is an inline scalar expression.

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

Piecewise mathematical function mapping input tuples to distinct output values.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Input Tuple ──► WHEN Condition 1 THEN Val 1 ... ELSE Default ──► Output Scalar
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'High' WHEN total_amount >= 250 THEN 'Medium' ELSE 'Low' END AS spend_tier FROM ecommerce.orders ORDER BY id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'High' WHEN total_amount >= 250 THEN 'Medium' ELSE 'Low' END AS spend_tier FROM ecommerce.orders ORDER BY id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, total_amount, CASE WHEN total_amount >= 1000 THEN 'High' WHEN total_amount >= 250 THEN 'Medium' ELSE 'Low' END AS spend_tier FROM ecommerce.orders ORDER BY id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT CASE WHEN total_amount > 100 THEN 'High' END FROM ecommerce.orders; -- Unhandled cases return NULL!
```

---

## 10. Debug It & Fix It

Always provide an explicit ELSE branch in production queries.

---

## 11. Evidence Ledger

```text
Lesson: Phase 10 — Case Expressions
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: CASE is an expression that returns a scalar value, not a procedural control-flow statement.
```

---

## 12. Exercises

Level 1: Categorize into 2 tiers.
Level 5: Use CASE inside SUM() for conditional aggregation.
