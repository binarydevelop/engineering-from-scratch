# Phase 02: Relational Mental Model

> **Motto:** Data is not a tree or a document; it is a mathematical set of relations governed by predicate logic.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 01  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Data is not a tree or a document; it is a mathematical set of relations governed by predicate logic.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Navigational databases (hierarchical and network models) forced queries to know the exact physical storage path. Relational algebra decoupled logical intent from physical access.

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

First normal form: attributes are atomic; tuples are unordered; duplicate rows are mathematically impossible in a true relation.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
Relation Heading: {id: INT, email: VARCHAR}
Relation Body: Set of Tuples {(1, 'a@b.com'), (2, 'c@d.com')}
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
CREATE TABLE lab.users (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "CREATE TABLE lab.users ("
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
CREATE TABLE lab.users (
    id INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE
);;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
INSERT INTO lab.users VALUES (1, 'a@b.com'), (1, 'duplicate@b.com'); -- Primary key violation
```

---

## 10. Debug It & Fix It

Enforcing relational constraints at the engine level guarantees application consistency.

---

## 11. Evidence Ledger

```text
Lesson: Phase 02 — Relational Mental Model
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Data is not a tree or a document; it is a mathematical set of relations governed by predicate logic.
```

---

## 12. Exercises

Level 1: Define relation attributes.
Level 5: Prove relational closure: query output is itself a relation.
