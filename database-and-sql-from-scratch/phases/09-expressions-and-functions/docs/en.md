# Phase 09: Expressions And Functions

> **Motto:** Compute close to the data to minimize network egress and application CPU cycles.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 08  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Compute close to the data to minimize network egress and application CPU cycles.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Pulling millions of raw rows into Node.js or Python to calculate basic totals destroys network bandwidth and memory.

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

Vectorized in-engine expression evaluation within the tuple projection loop.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Raw Attributes ──► [ In-Engine Function Call ] ──► Computed Value
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT sku, ROUND(price * 1.0825, 2) AS price_with_tax FROM ecommerce.products ORDER BY id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT sku, ROUND(price * 1.0825, 2) AS price_with_tax FROM ecommerce.products ORDER BY id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT sku, ROUND(price * 1.0825, 2) AS price_with_tax FROM ecommerce.products ORDER BY id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT price / 0 FROM ecommerce.products; -- Division by zero abort!
```

---

## 10. Debug It & Fix It

Use NULLIF(divisor, 0) to guard arithmetic.

---

## 11. Evidence Ledger

```text
Lesson: Phase 09 — Expressions And Functions
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Compute close to the data to minimize network egress and application CPU cycles.
```

---

## 12. Exercises

Level 1: Basic addition.
Level 5: Compare in-database aggregation vs client-side transformation.
