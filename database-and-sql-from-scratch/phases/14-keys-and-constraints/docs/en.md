# Phase 14: Keys And Constraints

> **Motto:** Constraints are the firewall of your database; your application code will fail, but constraints never sleep.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 13  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Constraints are the firewall of your database; your application code will fail, but constraints never sleep.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Relying solely on ORM validation allows race conditions, concurrent duplicate inserts, and orphaned child rows.

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

Declarative relational invariants verified atomically by the engine before tuple write completion.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
INSERT Tuple ──► [ Check Constraints -> PK Index Probe -> FK Parent Probe ] ──► Write Page
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
CREATE TABLE lab.accounts (
    id SERIAL PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0.00)
);
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "CREATE TABLE lab.accounts ("
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
CREATE TABLE lab.accounts (
    id SERIAL PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0.00)
);;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
INSERT INTO lab.accounts (balance) VALUES (-50.00); -- check constraint violation!
```

---

## 10. Debug It & Fix It

Enforce business rules directly in database DDL.

---

## 11. Evidence Ledger

```text
Lesson: Phase 14 — Keys And Constraints
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Constraints are the firewall of your database; your application code will fail, but constraints never sleep.
```

---

## 12. Exercises

Level 1: Add NOT NULL constraint.
Level 5: Measure CPU overhead of check constraints during bulk inserts.
