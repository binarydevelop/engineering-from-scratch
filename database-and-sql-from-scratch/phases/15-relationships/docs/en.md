# Phase 15: Relationships

> **Motto:** Foreign keys model physical relationships; cardinality determines query duplication risk.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 14  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Foreign keys model physical relationships; cardinality determines query duplication risk.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Misunderstanding relationship cardinality results in catastrophic Cartesian explosions during query joins.

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

Referential integrity constraints linking foreign key attributes in referencing relations to candidate keys in referenced relations.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
1:1 (Customer -> Profile)
1:N (Customer -> Orders)
N:M (Orders <-> OrderItems <-> Products)
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
SELECT o.id, c.email FROM ecommerce.orders o JOIN ecommerce.customers c ON o.customer_id = c.id ORDER BY o.id ASC;
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "SELECT o.id, c.email FROM ecommerce.orders o JOIN ecommerce.customers c ON o.customer_id = c.id ORDER BY o.id ASC;"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
SELECT o.id, c.email FROM ecommerce.orders o JOIN ecommerce.customers c ON o.customer_id = c.id ORDER BY o.id ASC;;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
INSERT INTO ecommerce.orders (customer_id) VALUES (9999); -- Foreign key violation!
```

---

## 10. Debug It & Fix It

Always verify referential integrity exists before loading child data.

---

## 11. Evidence Ledger

```text
Lesson: Phase 15 — Relationships
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Foreign keys model physical relationships; cardinality determines query duplication risk.
```

---

## 12. Exercises

Level 1: Map 1:N foreign key.
Level 5: Design a junction table with compound primary key for N:M relations.
