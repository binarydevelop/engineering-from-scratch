# Phase 11: String Querying

> **Motto:** Text querying without index strategy is a full-table sequential scan waiting to happen.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 10  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Text querying without index strategy is a full-table sequential scan waiting to happen.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

LIKE '%keyword%' cannot use standard B-Tree indexes, triggering catastrophic table scans at scale.

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

String pattern matching via finite state automata vs trigram/GIN index structures.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
LIKE 'abc%' -> B-Tree Range Search (Fast!)
LIKE '%abc%' -> Full Sequential Scan (Slow!)
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT id, name, sku FROM ecommerce.products WHERE name ILIKE '%phone%' ORDER BY id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT id, name, sku FROM ecommerce.products WHERE name ILIKE '%phone%' ORDER BY id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT id, name, sku FROM ecommerce.products WHERE name ILIKE '%phone%' ORDER BY id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
SELECT * FROM ecommerce.products WHERE LOWER(name) LIKE '%phone%'; -- Invalidates standard B-Tree on name
```

---

## 10. Debug It & Fix It

Use functional indexes or pg_trgm for arbitrary substring matching.

---

## 11. Evidence Ledger

```text
Lesson: Phase 11 — String Querying
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Text querying without index strategy is a full-table sequential scan waiting to happen.
```

---

## 12. Exercises

Level 1: Concatenate names.
Level 5: Compare B-Tree prefix search vs GIN trigram index search.
