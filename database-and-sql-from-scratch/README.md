# database-and-sql-from-scratch

<p align="center">
  <b>Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.</b>
</p>

<p align="center">
  <a href="VERSIONS.md"><img src="https://img.shields.io/badge/postgresql-16.4%20LTS-336791?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL 16.4"></a>
  <a href="ROADMAP.md"><img src="https://img.shields.io/badge/phases-102%20phases-3553ff?style=flat-square" alt="102 Phases"></a>
  <a href="exercises/"><img src="https://img.shields.io/badge/sql%20exercises-160%20problems-darkgreen?style=flat-square" alt="160 Exercises"></a>
  <a href="drills/"><img src="https://img.shields.io/badge/fluency%20drills-50%20drills-orange?style=flat-square" alt="50 Drills"></a>
  <a href="projects/"><img src="https://img.shields.io/badge/projects-7%20systems-purple?style=flat-square" alt="7 Projects"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-lightgrey?style=flat-square" alt="License"></a>
</p>

```text
░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒░░░▒▒▒
```

> **This is BOTH:**
>
> **a SQL course**
>
> **and**
>
> **a database engineering course.**
>
> Most engineers learn SQL as a collection of memorized clauses (`SELECT`, `JOIN`, `WHERE`), leaving the database engine as a mysterious black box. When a query returns duplicate rows, they blindly slap on `DISTINCT`. When a query slows down, they randomly add indexes.
>
> Conversely, traditional academic courses teach B-Tree balance factors, page splits, and Write-Ahead Logs, but never teach students how to systematically decompose a messy 5-part business requirement (like rolling 30-day cohort retention or top-3 products per category) into clean, high-performance declarative SQL.
>
> This curriculum bridges both worlds from first principles.

---

## The Dual Track Progression

```text
       SQL LANGUAGE                                     DATABASE ENGINEERING

          SELECT                                               SCHEMA
            │                                                    │
            ▼                                                    ▼
          FILTER                                            CONSTRAINTS
            │                                                    │
            ▼                                                    ▼
           JOIN                                               INDEXES
            │                                                    │
            ▼                                                    ▼
          GROUP                                             QUERY PLANS
            │                                                    │
            ▼                                                    ▼
         SUBQUERY                                           TRANSACTIONS
            │                                                    │
            ▼                                                    ▼
         WINDOWS                                            CONCURRENCY
            │                                                    │
            ▼                                                    ▼
        ANALYTICS                                             SCALING
            │                                                    │
            └─────────────────────────┬──────────────────────────┘
                                      ▼
                               DATABASE MASTERY
```

---

## The Core Philosophy: The Scientific Method for Data

Every phase and lesson in this repository enforces empirical inquiry:

```text
MOTTO ──► PROBLEM ──► PREDICT ──► FIRST PRINCIPLES ──► MENTAL MODEL 
  │
  └──► BUILD SCHEMA ──► WRITE SQL ──► RUN IT ──► INSPECT PLAN (EXPLAIN ANALYZE)
         │
         └──► MEASURE METRICS ──► BREAK IT ──► DEBUG IT ──► EVIDENCE LEDGER
```

For SQL queries specifically, you will never guess syntax. You will follow the **14-Question Query Thinking Framework** ([`docs/query-thinking.md`](docs/query-thinking.md)):

```text
 1. What should one output row represent (Grain)?
 2. Which tables contain the required facts?
 3. How are those tables related?
 4. What rows should be filtered before grouping (WHERE)?
 5. Do I need grouping (bucketing)?
 6. Do I need aggregation (collapsing rows into summaries)?
 7. Do I need calculations across rows (window functions)?
 8. Do I need ranking (ties, dense vs sparse)?
 9. Do I need existence or non-existence checks (EXISTS / NOT EXISTS)?
10. What ordering is required (deterministic tie-breakers)?
11. Could joins duplicate rows (1:N or N:M cardinality explosions)?
12. What happens with NULL (three-valued logic, outer joins, aggregates)?
13. What edge cases exist (zero orders, missing dates, refund reversions)?
14. How will this query behave as data grows from 1,000 to 10,000,000 rows?
```

---

## 5 Production-Grade Relational Datasets

All queries and exercises execute against real, multi-table relational schemas located in [`datasets/`](datasets/):

| Dataset | Schema | Key Entities | Purpose |
| :--- | :--- | :--- | :--- |
| **E-Commerce** | `ecommerce` | `customers`, `addresses`, `categories`, `products`, `inventory`, `orders`, `order_items`, `payments`, `refunds` | Retail transactions, hierarchical taxonomy, refunds, and inventory depletion |
| **Social Network** | `social` | `users`, `posts`, `follows`, `comments`, `likes` | Graph queries, mutual follows, chronological feeds, and lurker detection |
| **SaaS Multi-Tenant** | `saas` | `organizations`, `users`, `memberships`, `projects`, `events`, `subscriptions` | MRR calculations, seat utilization, churn heuristics, and JSONB telemetry |
| **Banking & Ledger**| `banking` | `customers`, `accounts`, `transactions`, `ledger_entries`, `audit_log` | Double-entry bookkeeping invariants, balance audits, and optimistic locking |
| **Clickstream** | `analytics` | `campaigns`, `sessions`, `events`, `user_cohorts` | 5-stage conversion funnels, monthly cohort retention, and gaps-and-islands |

---

## 7 Capstone Systems & Projects

Located in [`projects/`](projects/):

1. **[E-Commerce Database Engineering (Phase 87)](projects/01-ecommerce-database/):** Complete DDL, constraints, atomic checkout transactions with row-level locks, and 30 production business queries.
2. **[SQL Analytics Platform (Phase 88)](projects/02-sql-analytics-platform/):** Executive BI suite computing AOV, MoM revenue growth, conversion funnels, and rolling 7-day revenue.
3. **[Social Network Engine (Phase 89)](projects/03-social-network/):** Social graph traversal, mutual follow detection, feed generation, and Keyset Cursor pagination.
4. **[SaaS Multi-Tenant Engine (Phase 90)](projects/04-saas-metrics-engine/):** B2B tenant isolation, MRR waterfall reporting, seat caps, and GIN-indexed JSONB event querying.
5. **[Mini Relational Database in Python (Phase 97)](projects/05-mini-relational-db/):** In-memory relational engine implementing tables, primary key enforcement, secondary indexes, selection, projection, Nested Loop Join, and Hash Join.
6. **[Tiny Query Planner in Python (Phase 98)](projects/06-tiny-query-planner/):** Mathematical cost estimator proving why Sequential Scan beats Index Scan at high selectivity and choosing join strategies.
7. **[Production Database Application & Chaos Lab (Phase 99)](projects/07-production-db-app/):** FastAPI service with connection pool lifecycle, parameterized repositories, migrations, and chaos fault injection (deadlocks, pool exhaustion, lock contention).

---

## 210 Graded Exercises & Drills

1. **[160 Core Exercises (`exercises/`)](exercises/):**
   - **Beginner (40):** Projections, arithmetic, filtering, NULL handling, CASE expressions, deterministic sorting.
   - **Intermediate (50):** Multi-table joins, aggregations, HAVING thresholds, subqueries, EXISTS, CTEs, set operations.
   - **Advanced (40):** Window functions, ranking, LAG/LEAD, running totals, top-N per group, deduplication, gaps & islands, cohorts.
   - **Challenge (30):** High-stakes business modeling, reconciliation audits, RFM segmentation, Pareto distributions.
2. **[50 Fluency Drills (`drills/`)](drills/):**
   - 10 JOIN drills
   - 10 GROUP BY drills
   - 10 Date/Time drills
   - 10 Window Function drills
   - 10 Subquery & CTE drills
3. **Separate Solutions (`solutions/`):**
   - Reference answers are strictly separated from exercise prompts to encourage independent problem solving.

---

## Quickstart: Up and Running in 60 Seconds

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- `psql` (optional, can run directly inside Docker container)

### 1. Verify Your Environment
```bash
make env
```

### 2. Start Pinned PostgreSQL 16.4 Container
```bash
make up
```

### 3. Seed All 5 Production Datasets
```bash
make seed
```

### 4. Open Interactive SQL Terminal
```bash
make psql
```

### 5. Grade an Exercise or Drill
```bash
# Grade a single exercise
python3 scripts/grade-query.py exercises/beginner/q01-select-constants.md

# Grade all 50 fluency drills
make drills
```

### 6. Run Python Relational Engine Tests
```bash
python3 projects/05-mini-relational-db/test_engine.py
python3 projects/06-tiny-query-planner/test_planner.py
```

---

## Core Documentation

- **[`docs/query-thinking.md`](docs/query-thinking.md):** The 14-Question Query Thinking Framework.
- **[`docs/explain-guide.md`](docs/explain-guide.md):** How to read and measure `EXPLAIN (ANALYZE, BUFFERS)`.
- **[`docs/mental-models.md`](docs/mental-models.md):** Relational algebra, 8KB heap pages, B-Trees, MVCC, and query optimizers.
- **[`docs/sql-reference.md`](docs/sql-reference.md):** Standard SQL vs PostgreSQL extensions.
- **[`docs/glossary.md`](docs/glossary.md):** Exact relational engineering definitions vs common industry misconceptions.
- **[`docs/troubleshooting.md`](docs/troubleshooting.md):** Classic SQL traps, deadlock diagnosis, and performance debugging.
- **[`VERSIONS.md`](VERSIONS.md):** Pinned PostgreSQL 16.4 specifications and architectural distinction boundaries.

---

## The Final Standard

> SQL is no longer a collection of clauses, and the database is no longer a black box.
>
> We learned to translate business questions into relational operations, write increasingly sophisticated queries, model relationships correctly, understand how those queries are physically executed, and reason about indexes, transactions, concurrency, and performance.
>
> Now when we are given data and a question, we can query it. When the query becomes slow, we can diagnose it. When the schema becomes complicated, we can model it. And when a relational database appears inside a system architecture, we understand what it is doing and why.
