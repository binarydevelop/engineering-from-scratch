# Curriculum Roadmap: 102 Phases to Database & SQL Mastery

> **Repository Motto:** Understand it. Model it. Query it. Inspect it. Measure it. Break it. Fix it. Optimize it. Ship it.

This roadmap details the progression across both tracks: **Track A (SQL Query Language)** and **Track B (Database Engineering & Systems Internals)**.

---

## High-Level Curriculum Progression

```text
       TRACK A: SQL LANGUAGE                           TRACK B: DATABASE ENGINEERING
       ─────────────────────                           ──────────────────────────────
PART 1: FOUNDATIONS & LAB SETUP
  ├── Phase 00: Environment & SQL Lab             ├── Phase 01: Why Databases Exist
  ├── Phase 03: SQL Query Anatomy                 └── Phase 02: Relational Mental Model
  │
PART 2: SINGLE-RELATION QUERYING & DDL
  ├── Phase 04: SELECT Deeply                     ├── Phase 13: Data Modification (DML)
  ├── Phase 05: WHERE Deeply                      ├── Phase 14: Keys & Constraints
  ├── Phase 06: NULL & 3-Valued Logic             └── Phase 15: Entity Relationships
  ├── Phase 07: ORDER BY
  ├── Phase 08: LIMIT / FETCH / Pagination
  ├── Phase 09: Expressions & Functions
  ├── Phase 10: CASE Expressions
  ├── Phase 11: String Querying
  └── Phase 12: Date & Time SQL
  │
PART 3: MULTI-TABLE JOINS & RELATIONAL INTEGRITY
  ├── Phase 16: INNER JOIN From First Principles  ├── Phase 19: Join Cardinality
  ├── Phase 17: LEFT JOIN                         └── Phase 20: Join Debugging Lab
  └── Phase 18: RIGHT & FULL JOIN
  │
PART 4: AGGREGATIONS, GROUPING & PROCESSING ORDER
  ├── Phase 21: Aggregate Functions               ├── Phase 25: Logical SQL Processing Order
  ├── Phase 22: GROUP BY                          └── Phase 26: DISTINCT Truths & Traps
  ├── Phase 23: HAVING
  └── Phase 24: Conditional Aggregation
  │
PART 5: SUBQUERIES, SETS & CTES
  ├── Phase 27: Subqueries (Scalar, Column, Table)├── Phase 31: Set Operations (UNION, EXCEPT)
  ├── Phase 28: Correlated Subqueries             ├── Phase 32: Common Table Expressions (CTEs)
  ├── Phase 29: EXISTS & NOT EXISTS               └── Phase 33: Recursive CTEs (Hierarchies)
  └── Phase 30: IN and NOT IN (NULL Traps)
  │
PART 6: WINDOW FUNCTIONS & ANALYTICAL SQL
  ├── Phase 34: Window Functions Mental Model     ├── Phase 41: Top-N Per Group
  ├── Phase 35: ROW_NUMBER                        ├── Phase 42: Deduplication Patterns
  ├── Phase 36: RANK & DENSE_RANK                 ├── Phase 43: Gaps and Islands
  ├── Phase 37: PARTITION BY                      ├── Phase 44: Pivot-Like Reporting
  ├── Phase 38: LAG and LEAD                      ├── Phase 45: Conversion Funnels
  ├── Phase 39: Running Totals                    ├── Phase 46: Cohort Analysis
  └── Phase 40: Window Frames (ROWS vs RANGE)     └── Phase 47: Retention Analysis
  │
  └── [ Phase 48: Query Challenge Set I (30 Core Business Problems) ]
  │
PART 7: RELATIONAL MODELING & NORMALIZATION
  ├── Phase 49: Schema Design Principles          ├── Phase 50: Normalization (1NF -> 3NF)
  └── Phase 51: Denormalization Tradeoffs
  │
PART 8: STORAGE, INDEXES & THE QUERY OPTIMIZER
  ├── Phase 52: Indexes from First Principles     ├── Phase 57: Index Selectivity
  ├── Phase 53: B-Tree Internals (Pages & Blocks) ├── Phase 58: Composite Indexes
  ├── Phase 54: EXPLAIN Plan Reading              ├── Phase 59: Partial & Expression Indexes
  ├── Phase 55: EXPLAIN ANALYZE Execution Profiling├── Phase 60: The Query Planner & Costing
  ├── Phase 56: Sequential Scan vs Index Scan     ├── Phase 61: Join Algorithms (Hash/Merge/NL)
  ├── Phase 62: Sorting & work_mem Spills         ├── Phase 63: Aggregation Internals
  └── Phase 64: Performance Query Lab
  │
PART 9: TRANSACTIONS, CONCURRENCY & MVCC
  ├── Phase 65: Transactions (BEGIN, COMMIT)     ├── Phase 69: Lock Modes & Row Locking
  ├── Phase 66: ACID Guarantees Experimentally    ├── Phase 70: Deadlock Diagnosis & Fixes
  ├── Phase 67: Concurrent Sessions Lab           ├── Phase 71: MVCC (xmin, xmax, Vacuum)
  └── Phase 68: Isolation Levels (Read Committed, Repeatable Read, Serializable)
  │
  ├── Phase 72: Optimistic Concurrency Control    └── Phase 73: Connection Pooling
  │
  └── [ Phase 74: Query Challenge Set II (40 Intermediate/Advanced Problems) ]
  │
PART 10: PRODUCTION RELATIONAL PATTERNS & SCALING
  ├── Phase 75: Deep Pagination Traps             ├── Phase 80: Table Partitioning
  ├── Phase 76: Keyset Cursor Pagination          ├── Phase 81: Replication & Read Replicas
  ├── Phase 77: Views                             ├── Phase 82: Backup, WAL & Disaster Recovery
  ├── Phase 78: Materialized Views                ├── Phase 83: SQL Injection Vulnerabilities
  ├── Phase 79: JSON / JSONB Semi-Structured Data ├── Phase 84: ORMs & Generated SQL Inspection
  ├── Phase 85: The N+1 Query Problem             └── Phase 86: Database Migrations
  │
PART 11: FULL-SCALE CAPSTONE PROJECTS
  ├── Phase 87: Project 01 — E-Commerce Database (30 Business Queries)
  ├── Phase 88: Project 02 — SQL Analytics Platform (Cohorts, Funnels, MoM)
  ├── Phase 89: Project 03 — Social Network Engine (Graph Feeds & Keyset Cursors)
  └── Phase 90: Project 04 — SaaS Multi-Tenant Engine (MRR, Seats, JSONB)
  │
  └── [ Phase 91: Query Challenge Set III (50 Real-World Interview Problems) ]
  │
PART 12: ARCHITECTURE, ENGINE BUILDING & FINAL MASTERY
  ├── Phase 92: SQL Style & Readability           ├── Phase 95: When Relational Databases Are Wrong
  ├── Phase 93: Query Rewriting & Equivalences    ├── Phase 96: Relational DBs in System Design
  └── Phase 94: Classic Database Anti-Patterns
  │
  ├── Phase 97: Project 05 — Build Mini Relational Database in Python
  ├── Phase 98: Project 06 — Build Tiny Query Planner in Python
  └── Phase 99: Project 07 — Production-Like Database Application & Chaos Lab
  │
  ├── Phase 100: Final Query Mastery Challenge (50 Independent Capstone Problems)
  └── Phase 101: The Final Mental Model (Dual-Track Synthesis)
```

---

## Detailed Directory Map of All 102 Phases

| Phase | Directory | Topic | Track |
| :--- | :--- | :--- | :--- |
| **00** | [`phases/00-environment-and-sql-lab/`](phases/00-environment-and-sql-lab/) | Environment & SQL Lab | Foundations |
| **01** | [`phases/01-why-databases-exist/`](phases/01-why-databases-exist/) | Why Databases Exist | Engineering |
| **02** | [`phases/02-relational-mental-model/`](phases/02-relational-mental-model/) | Relational Mental Model | Foundations |
| **03** | [`phases/03-sql-query-anatomy/`](phases/03-sql-query-anatomy/) | SQL Query Anatomy | SQL Language |
| **04** | [`phases/04-select-deeply/`](phases/04-select-deeply/) | SELECT Deeply | SQL Language |
| **05** | [`phases/05-where-deeply/`](phases/05-where-deeply/) | WHERE Deeply | SQL Language |
| **06** | [`phases/06-null-and-three-valued-logic/`](phases/06-null-and-three-valued-logic/) | NULL & 3-Valued Logic | SQL Language |
| **07** | [`phases/07-order-by/`](phases/07-order-by/) | ORDER BY & Determinism | SQL Language |
| **08** | [`phases/08-limit-fetch-pagination/`](phases/08-limit-fetch-pagination/) | LIMIT & Pagination Intro | SQL Language |
| **09** | [`phases/09-expressions-and-functions/`](phases/09-expressions-and-functions/) | Expressions & Functions | SQL Language |
| **10** | [`phases/10-case-expressions/`](phases/10-case-expressions/) | CASE Expressions | SQL Language |
| **11** | [`phases/11-string-querying/`](phases/11-string-querying/) | String Querying & Text | SQL Language |
| **12** | [`phases/12-date-and-time-sql/`](phases/12-date-and-time-sql/) | Date & Time SQL | SQL Language |
| **13** | [`phases/13-data-modification/`](phases/13-data-modification/) | Data Modification (DML) | Engineering |
| **14** | [`phases/14-keys-and-constraints/`](phases/14-keys-and-constraints/) | Keys & Constraints | Engineering |
| **15** | [`phases/15-relationships/`](phases/15-relationships/) | Entity Relationships | Engineering |
| **16** | [`phases/16-inner-join-from-first-principles/`](phases/16-inner-join-from-first-principles/) | INNER JOIN First Principles | SQL Language |
| **17** | [`phases/17-left-join/`](phases/17-left-join/) | LEFT JOIN & Outer Joins | SQL Language |
| **18** | [`phases/18-right-full-join/`](phases/18-right-full-join/) | RIGHT & FULL OUTER JOIN | SQL Language |
| **19** | [`phases/19-join-cardinality/`](phases/19-join-cardinality/) | Join Cardinality (1:N, N:M) | Engineering |
| **20** | [`phases/20-join-debugging/`](phases/20-join-debugging/) | Join Debugging Lab | Engineering |
| **21** | [`phases/21-aggregate-functions/`](phases/21-aggregate-functions/) | Aggregate Functions | SQL Language |
| **22** | [`phases/22-group-by/`](phases/22-group-by/) | GROUP BY & Bucketing | SQL Language |
| **23** | [`phases/23-having/`](phases/23-having/) | HAVING Filter Clauses | SQL Language |
| **24** | [`phases/24-conditional-aggregation/`](phases/24-conditional-aggregation/) | Conditional Aggregation | SQL Language |
| **25** | [`phases/25-logical-sql-processing-order/`](phases/25-logical-sql-processing-order/) | Logical Processing Order | Engineering |
| **26** | [`phases/26-distinct/`](phases/26-distinct/) | DISTINCT & De-duplication | SQL Language |
| **27** | [`phases/27-subqueries/`](phases/27-subqueries/) | Subqueries & Derived Tables | SQL Language |
| **28** | [`phases/28-correlated-subqueries/`](phases/28-correlated-subqueries/) | Correlated Subqueries | SQL Language |
| **29** | [`phases/29-exists-not-exists/`](phases/29-exists-not-exists/) | EXISTS / NOT EXISTS | SQL Language |
| **30** | [`phases/30-in-and-not-in/`](phases/30-in-and-not-in/) | IN / NOT IN & NULL Traps | SQL Language |
| **31** | [`phases/31-set-operations/`](phases/31-set-operations/) | Set Operations (UNION, EXCEPT)| SQL Language |
| **32** | [`phases/32-ctes/`](phases/32-ctes/) | Common Table Expressions | SQL Language |
| **33** | [`phases/33-recursive-ctes/`](phases/33-recursive-ctes/) | Recursive CTEs & Graphs | SQL Language |
| **34** | [`phases/34-window-functions-mental-model/`](phases/34-window-functions-mental-model/) | Window Functions Mental Model| SQL Language |
| **35** | [`phases/35-row-number/`](phases/35-row-number/) | ROW_NUMBER Ordering | SQL Language |
| **36** | [`phases/36-rank-and-dense-rank/`](phases/36-rank-and-dense-rank/) | RANK and DENSE_RANK | SQL Language |
| **37** | [`phases/37-partition-by/`](phases/37-partition-by/) | PARTITION BY Scopes | SQL Language |
| **38** | [`phases/38-lag-and-lead/`](phases/38-lag-and-lead/) | LAG & LEAD Time Travel | SQL Language |
| **39** | [`phases/39-running-totals/`](phases/39-running-totals/) | Running Totals & Cumulative | SQL Language |
| **40** | [`phases/40-window-frames/`](phases/40-window-frames/) | Window Frames (ROWS/RANGE) | SQL Language |
| **41** | [`phases/41-top-n-per-group/`](phases/41-top-n-per-group/) | Top-N Per Group Problems | SQL Language |
| **42** | [`phases/42-deduplication/`](phases/42-deduplication/) | Event Deduplication | SQL Language |
| **43** | [`phases/43-gaps-and-islands/`](phases/43-gaps-and-islands/) | Gaps and Islands Analysis | SQL Language |
| **44** | [`phases/44-pivot-like-queries/`](phases/44-pivot-like-queries/) | Pivot-Like Reporting | SQL Language |
| **45** | [`phases/45-funnel-queries/`](phases/45-funnel-queries/) | Conversion Funnels | SQL Language |
| **46** | [`phases/46-cohort-queries/`](phases/46-cohort-queries/) | Cohort Retention Matrices | SQL Language |
| **47** | [`phases/47-retention-analysis/`](phases/47-retention-analysis/) | Retention (Day 1, 7, 30) | SQL Language |
| **48** | [`phases/48-query-challenge-set-i/`](phases/48-query-challenge-set-i/) | Challenge Set I | Verification |
| **49** | [`phases/49-schema-design/`](phases/49-schema-design/) | Schema Design Principles | Engineering |
| **50** | [`phases/50-normalization/`](phases/50-normalization/) | Normalization (1NF, 2NF, 3NF)| Engineering |
| **51** | [`phases/51-denormalization/`](phases/51-denormalization/) | Denormalization Tradeoffs | Engineering |
| **52** | [`phases/52-indexes-from-first-principles/`](phases/52-indexes-from-first-principles/) | Indexes from First Principles | Engineering |
| **53** | [`phases/53-b-tree/`](phases/53-b-tree/) | B-Tree Internals & Layout | Engineering |
| **54** | [`phases/54-explain/`](phases/54-explain/) | Reading EXPLAIN Plans | Engineering |
| **55** | [`phases/55-explain-analyze/`](phases/55-explain-analyze/) | EXPLAIN ANALYZE Profiling | Engineering |
| **56** | [`phases/56-sequential-scan-vs-index-scan/`](phases/56-sequential-scan-vs-index-scan/) | Seq Scan vs Index Scan | Engineering |
| **57** | [`phases/57-index-selectivity/`](phases/57-index-selectivity/) | Index Selectivity Ratios | Engineering |
| **58** | [`phases/58-composite-indexes/`](phases/58-composite-indexes/) | Composite Indexes & Order | Engineering |
| **59** | [`phases/59-partial-specialized-indexes/`](phases/59-partial-specialized-indexes/) | Partial & GIN Indexes | Engineering |
| **60** | [`phases/60-query-planner/`](phases/60-query-planner/) | Query Optimizer & Costing | Engineering |
| **61** | [`phases/61-join-algorithms/`](phases/61-join-algorithms/) | Join Algorithms (NL/Hash/Merge)| Engineering |
| **62** | [`phases/62-sorting-and-memory/`](phases/62-sorting-and-memory/) | Sorting & work_mem Disk Spills| Engineering |
| **63** | [`phases/63-aggregation-internals/`](phases/63-aggregation-internals/) | Aggregation Internals | Engineering |
| **64** | [`phases/64-performance-query-lab/`](phases/64-performance-query-lab/) | 10 Slow Queries Lab | Engineering |
| **65** | [`phases/65-transactions/`](phases/65-transactions/) | Transactions & Atomic Writes | Engineering |
| **66** | [`phases/66-acid/`](phases/66-acid/) | ACID Properties Lab | Engineering |
| **67** | [`phases/67-concurrent-sessions/`](phases/67-concurrent-sessions/) | Multi-Client Sessions | Engineering |
| **68** | [`phases/68-isolation-levels/`](phases/68-isolation-levels/) | Isolation Levels & Anomalies | Engineering |
| **69** | [`phases/69-locks/`](phases/69-locks/) | Row & Table Lock Modes | Engineering |
| **70** | [`phases/70-deadlocks/`](phases/70-deadlocks/) | Deadlock Reproduction & Fix | Engineering |
| **71** | [`phases/71-mvcc/`](phases/71-mvcc/) | MVCC (xmin, xmax, Vacuum) | Engineering |
| **72** | [`phases/72-optimistic-concurrency/`](phases/72-optimistic-concurrency/) | Optimistic Concurrency Control| Engineering |
| **73** | [`phases/73-connection-pools/`](phases/73-connection-pools/) | Connection Pool Architecture | Engineering |
| **74** | [`phases/74-query-challenge-set-ii/`](phases/74-query-challenge-set-ii/) | Challenge Set II | Verification |
| **75** | [`phases/75-pagination/`](phases/75-pagination/) | Deep Pagination Bottlenecks | Engineering |
| **76** | [`phases/76-keyset-pagination/`](phases/76-keyset-pagination/) | Keyset Cursor Pagination | Engineering |
| **77** | [`phases/77-views/`](phases/77-views/) | Logical Views | Engineering |
| **78** | [`phases/78-materialized-views/`](phases/78-materialized-views/) | Materialized Views & Refresh | Engineering |
| **79** | [`phases/79-json-jsonb/`](phases/79-json-jsonb/) | JSON / JSONB Semi-Structured | Engineering |
| **80** | [`phases/80-partitioning/`](phases/80-partitioning/) | Table Partitioning & Pruning | Engineering |
| **81** | [`phases/81-replication/`](phases/81-replication/) | Replication Topologies | Engineering |
| **82** | [`phases/82-backup-and-restore/`](phases/82-backup-and-restore/) | Backups vs Replication | Engineering |
| **83** | [`phases/83-sql-injection/`](phases/83-sql-injection/) | SQL Injection & Parameterization| Engineering |
| **84** | [`phases/84-orm-and-generated-sql/`](phases/84-orm-and-generated-sql/) | ORM Abstractions & Leaks | Engineering |
| **85** | [`phases/85-n-plus-one-queries/`](phases/85-n-plus-one-queries/) | N+1 Queries & Batch Loading | Engineering |
| **86** | [`phases/86-database-migrations/`](phases/86-database-migrations/) | Zero-Downtime Schema Evolution| Engineering |
| **87** | [`phases/87-ecommerce-project/`](phases/87-ecommerce-project/) | Project 01: E-Commerce Platform| Capstone |
| **88** | [`phases/88-sql-analytics-project/`](phases/88-sql-analytics-project/) | Project 02: SQL Analytics Suite| Capstone |
| **89** | [`phases/89-social-network-project/`](phases/89-social-network-project/) | Project 03: Social Network Engine| Capstone |
| **90** | [`phases/90-saas-project/`](phases/90-saas-project/) | Project 04: SaaS Multi-Tenant Engine| Capstone |
| **91** | [`phases/91-query-challenge-set-iii/`](phases/91-query-challenge-set-iii/) | Challenge Set III | Verification |
| **92** | [`phases/92-sql-style-and-readability/`](phases/92-sql-style-and-readability/) | SQL Formatting & Readability | Engineering |
| **93** | [`phases/93-query-rewriting/`](phases/93-query-rewriting/) | Query Rewriting Equivalences | Engineering |
| **94** | [`phases/94-database-anti-patterns/`](phases/94-database-anti-patterns/) | Relational Anti-Patterns | Engineering |
| **95** | [`phases/95-when-relational-databases-are-wrong/`](phases/95-when-relational-databases-are-wrong/) | When RDBMS Is the Wrong Tool | Architecture |
| **96** | [`phases/96-database-in-system-design/`](phases/96-database-in-system-design/) | Databases in System Design | Architecture |
| **97** | [`phases/97-build-mini-relational-db/`](phases/97-build-mini-relational-db/) | Project 05: Build Mini RDBMS | Internals |
| **98** | [`phases/98-build-tiny-query-planner/`](phases/98-build-tiny-query-planner/) | Project 06: Build Tiny Planner | Internals |
| **99** | [`phases/99-production-like-database-app/`](phases/99-production-like-database-app/) | Project 07: Production DB App | Production |
| **100**| [`phases/100-final-query-mastery-challenge/`](phases/100-final-query-mastery-challenge/)| Capstone Challenge (50 Queries) | Mastery |
| **101**| [`phases/101-final-mental-model/`](phases/101-final-mental-model/) | The Unified Final Mental Model | Mastery |
