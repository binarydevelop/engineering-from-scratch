# The Learning Philosophy: Relational Engineering & SQL Mastery

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

---

## 1. Why This Repository Exists

Most database curricula suffer from one of two fatal pedagogical flaws:

1. **The Syntax Illusion:** They treat SQL as a set of memorizable text templates (`SELECT`, `FROM`, `WHERE`). Learners are taught syntax in isolation without understanding relational algebra, row grain, or how the engine scans, filters, and joins data. When a query returns duplicated rows or runs for 45 minutes in production, the learner has zero diagnostic tools.
2. **The Ivory Tower of Internals:** They focus exclusively on B-tree balance factors, page splits, write-ahead logs, and buffer pool eviction algorithms, but never train the learner to fluently translate a messy 5-part business requirement (like rolling 30-day cohort retention or top-3 products per category) into clean, high-performance declarative SQL.

**`database-and-sql-from-scratch` rejects this false dichotomy.**

SQL and Relational Database Engines are two sides of the same mechanical coin:
- **SQL** is the declarative language through which you express *what* mathematical relation you need.
- **The Database Engine** is the distributed, physical computing system that figures out *how* to materialize that relation against persistent storage without corrupting data or exhausting RAM.

---

## 2. The Two Parallel Learning Tracks

This curriculum advances along two parallel tracks that cross-pollinate continuously and eventually merge into unified database mastery:

```text
TRACK A: SQL LANGUAGE                           TRACK B: DATABASE ENGINEERING
─────────────────────                           ──────────────────────────────
Phase 03: Query Anatomy                         Phase 01: Why Databases Exist
Phase 04: SELECT Deeply                         Phase 02: Relational Mental Model
Phase 05: WHERE Deeply                          Phase 14: Keys & Constraints
Phase 06: NULL & 3-Valued Logic                 Phase 15: Relationships & Cardinality
Phase 07: ORDER BY                              Phase 49: Normalization (1NF -> 3NF)
Phase 16-20: Joins (Inner, Left, Cross)         Phase 52: Indexes from First Principles
Phase 21-24: Aggregations & Grouping            Phase 53: B-Trees & Storage Pages
Phase 27-30: Subqueries & Existence             Phase 54-55: EXPLAIN & EXPLAIN ANALYZE
Phase 31-33: CTEs & Recursion                   Phase 60: Query Planner Cost Estimation
Phase 34-42: Window Functions & Analytics       Phase 61: Join Algorithms (Hash/Merge/NL)
Phase 43-47: Funnels, Cohorts, Gaps & Islands   Phase 65-72: Transactions, ACID, MVCC, Locks
Phase 75-76: Keyset Pagination                  Phase 80-82: Partitioning, Replication, Backups
Phase 92-93: Query Rewriting                    Phase 83-86: Migrations, ORMs & N+1 Queries
                 │                                               │
                 └───────────────────────┬───────────────────────┘
                                         ▼
                             UNIFIED DATABASE MASTERY
                                 Phases 87 - 101
                     E-Commerce, Social, SaaS Capstones
                     Mini-Relational DB & Planner Engines
                     Production Database Applications
```

---

## 3. The 14-Question Query Thinking Framework

Whenever you are presented with a real-world analytical question or application feature, **never begin by typing SQL syntax**. Instead, walk through the 14 structural questions defined in [`docs/query-thinking.md`](docs/query-thinking.md):

```text
 1. What should one output row represent (Grain)?
 2. Which tables contain the required facts?
 3. How are those tables related?
 4. What rows should be filtered before grouping?
 5. Do I need grouping (bucketing)?
 6. Do I need aggregation (collapsing rows into summaries)?
 7. Do I need calculations across rows (windowing)?
 8. Do I need ranking (ties, dense vs sparse)?
 9. Do I need existence or non-existence checks?
10. What ordering is required (deterministic tie-breakers)?
11. Could joins duplicate rows (1:N or N:M cardinality explosions)?
12. What happens with NULL (three-valued logic, outer joins, aggregates)?
13. What edge cases exist (zero orders, missing dates, refund reversions)?
14. How will this query behave as data grows from 1,000 to 100,000,000 rows?
```

---

## 4. The 5-Level Exercise Progression

Every query topic features exercises graded across 5 progressive levels of engineering depth:

1. **Level 1 — Direct:** Pure syntax application to verify comprehension of the clause.
2. **Level 2 — Combination:** Merging the clause with earlier concepts (e.g., `WHERE` + `GROUP BY` + `JOIN`).
3. **Level 3 — Edge Case:** Trap identification (e.g., zero-order customers, `NULL` handling, duplicate elimination).
4. **Level 4 — Realistic:** Translating an ambiguous, multi-sentence executive business requirement into exact SQL.
5. **Level 5 — Performance-Aware:** Analyzing `EXPLAIN (ANALYZE, BUFFERS)` to diagnose sequential scans, eliminate temporary disk spills, and construct optimal indexes.

---

## 5. The Lesson Loop

Every lesson follows this empirical cadence:

```text
MOTTO ──► PROBLEM ──► PREDICT ──► FIRST PRINCIPLES ──► MENTAL MODEL 
  │
  └──► BUILD SCHEMA ──► WRITE SQL ──► RUN IT ──► INSPECT PLAN 
         │
         └──► MEASURE METRICS ──► BREAK IT ──► DEBUG IT ──► EVIDENCE LEDGER
```

By keeping an **Evidence Ledger** in every lesson, you build an unshakeable instinct for query costs, buffer hits, join memory footprints, and row selectivity.
