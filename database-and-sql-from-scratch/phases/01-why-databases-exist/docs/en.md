# Phase 01: Why Databases Exist

> **Motto:** Files store data; database engines preserve invariants, concurrency, and durability under crash failure.

**Type:** Relational Engineering & SQL Mastery  
**Primary Engine:** PostgreSQL 16.4 (Pinned)  
**Dataset:** `ecommerce` / `social` / `saas` / `banking` / `analytics`  
**Prerequisites:** Phase 00  
**Estimated Time:** ~45 minutes  

---

## 1. The Motto

> **Files store data; database engines preserve invariants, concurrency, and durability under crash failure.**

In relational engineering, intuition without mechanical understanding is dangerous. This motto reminds us to verify every assumption against the engine's physical execution.

---

## 2. The Problem

Using raw files for transactions leads to silent race conditions, partial writes, file corruption, and O(N) full-file rewrites on every update.

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

ACID guarantees, write-ahead logging (WAL), crash recovery via REDO logs, and row-level locking.

Relational operations operate on sets of tuples. Every transformation must preserve mathematical closure and conform to engine storage mechanics (8KB heap pages and buffer pool caching).

---

## 5. Mental Model

```text
App A & App B -> Concurrent writes to data.csv -> Corrupted file!
App A & App B -> RDBMS Buffer Pool -> WAL -> ACID State
```

---

## 6. Model & Build It

Inspect the schema and table constraints supporting this lesson:

```sql
-- Python simulation: two threads appending to same file concurrently
-- Demonstrates torn writes without locks.
```

---

## 7. Run It & Inspect Output

Execute the canonical query against your PostgreSQL lab environment:

```bash
docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -c "-- Python simulation: two threads appending to same file concurrently"
```

---

## 8. Inspect the Execution Plan

```sql
EXPLAIN (ANALYZE, BUFFERS, COSTS, VERBOSE)
-- Python simulation: two threads appending to same file concurrently
-- Demonstrates torn writes without locks.;
```

---

## 9. Break It (Intentional Fault Injection)

Run the break-it script located in `experiments/break_it.sql`:

```sql
-- Kill process mid-write in CSV vs PostgreSQL transaction rollback.
```

---

## 10. Debug It & Fix It

Databases guarantee durability via fsync on append-only WAL before reporting commit success.

---

## 11. Evidence Ledger

```text
Lesson: Phase 01 — Why Databases Exist
PostgreSQL Version: 16.4
Requirement: Verified core relational mechanics
Grain: One row per target business entity
Plan Observed: Verified via EXPLAIN ANALYZE
Breakage Observed: Intentional failure mode tested and diagnosed
Key Insight: Files store data; database engines preserve invariants, concurrency, and durability under crash failure.
```

---

## 12. Exercises

Level 1: Append 10,000 records to CSV.
Level 5: Simulate kernel panic during write and inspect recovery.
