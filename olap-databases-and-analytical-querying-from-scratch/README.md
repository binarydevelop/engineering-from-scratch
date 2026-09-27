# OLAP Databases and Analytical Querying from Scratch

> **Understand it. Model it. Query it. Scan it. Aggregate it. Measure it. Break it. Optimize it. Scale it.**

```text
This is NOT a ClickHouse tutorial.

This is NOT a data warehouse certification course.

This is NOT a list of analytical SQL functions.

This is a course in understanding how analytical databases
store, execute, optimize, and serve large analytical workloads.
```

---

## The Central Mental Model

```text
OLTP                                      OLAP
──────────────────────────────────        ──────────────────────────────────
many small operations                     fewer but larger queries
       ↓                                         ↓
point lookup / narrow range               scan many rows
       ↓                                         ↓
individual rows                           read a subset of columns
       ↓                                         ↓
frequent writes                           filter
       ↓                                         ↓
transactions                              group
                                                 ↓
                                          aggregate
                                                 ↓
                                          join
                                                 ↓
                                          produce analytical result
```

```text
OLAP ≠ "SQL but on more data"
```

The storage engine, execution model, data layout, and ingestion strategy often differ substantially.

---

## Primary Learning Progression

```text
Analytical Questions
       ↓
Analytical SQL
       ↓
Row vs Column
       ↓
Compression
       ↓
Vectorized Execution
       ↓
Parquet
       ↓
Partitioning
       ↓
Data Skipping
       ↓
Query Planning
       ↓
Joins / Aggregation
       ↓
DuckDB
       ↓
ClickHouse
       ↓
Real-Time OLAP
       ↓
Druid / Pinot
       ↓
Distributed Execution
       ↓
Production Analytics
```

---

## Two Parallel Tracks

```text
TRACK A — Analytical Querying             TRACK B — OLAP Database Engineering
───────────────────────────────            ────────────────────────────────────
SELECT                                     row storage
  ↓                                          ↓
filters                                    column storage
  ↓                                          ↓
aggregations                               compression
  ↓                                          ↓
GROUP BY / HAVING                          vectorized execution
  ↓                                          ↓
joins & star schemas                       zones & data skipping
  ↓                                          ↓
window functions                           partitioning
  ↓                                          ↓
rollups & percentiles                      query planning
  ↓                                          ↓
time-series analytics                      parallel execution
  ↓                                          ↓
funnel queries                             distributed aggregation
  ↓                                          ↓
cohorts & retention                        ingestion pipelines
  ↓                                          ↓
sessionization                             materialization
  ↓                                          ↓
approximate analytics                      real-time serving

                         ═════════════════════════════
                                MERGED MASTERY:
                         Analytical SQL
                                +
                         Storage Internals
                                +
                         Query Execution
                                ↓
                         OLAP Engineering
```

---

## Repository Structure

```text
olap-databases-and-analytical-querying-from-scratch/
├── README.md                           # Master curriculum & architectural philosophy
├── ROADMAP.md                          # Complete 32-part, 246-phase curriculum syllabus
├── LEARNING.md                         # The 15 cognitive invariants and core query loop
├── LESSON_TEMPLATE.md                  # Strict 21-section lesson template & evidence artifact
├── QUERY_TEMPLATE.md                   # Analytical query contract with physical predictions
├── BENCHMARK_TEMPLATE.md               # Rigorous benchmark specification (zero theater)
├── VERSIONS.md                         # Technology stack, pinned versions, driver matrix
├── CONTRIBUTING.md                     # Evidence standards and contribution workflow
├── .gitignore                          # Artifact exclusions and cache rules
├── .env.example                        # Environment variables for ports and credentials
├── Makefile                            # Reproducible lab automation targets
├── docker-compose.yml                  # Pinned ClickHouse 24.8 & PostgreSQL 16.4 services
├── requirements.txt                    # Pinned Python analytical drivers
│
├── scripts/
│   ├── check-environment.sh            # Pre-flight environment & port verification
│   ├── generate-data.py                # Multi-domain synthetic analytical data generator
│   ├── start-lab.sh                    # Container launch, health check, and dataset priming
│   ├── stop-lab.sh                     # Tear down all lab containers
│   ├── reset-data.sh                   # Clean and regenerate fresh analytical states
│   └── benchmark.py                    # Multi-engine reproducible benchmark runner
│
├── datasets/                           # 6 Core Analytical Domain Datasets (Parquet + CSV)
│   ├── ecommerce/                      # fact_order_items, dim_users, dim_products
│   ├── clickstream/                    # web_events (views, carts, purchases)
│   ├── observability/                  # service_logs (spans, latencies, error codes)
│   ├── ads/                            # ad_impressions (bids, CPM, CTR, conversions)
│   ├── finance/                        # financial_transactions (amounts, fraud, fees)
│   └── iot/                            # sensor_readings (temperatures, pressure, alerts)
│
├── duckdb/                             # DuckDB in-process analytical suite
│   ├── schemas/                        # DDL statements for analytical tables
│   ├── queries/                        # Advanced analytical queries and funnels
│   └── experiments/                    # In-memory vector chunk inspection
│
├── clickhouse/                         # Production columnar DBMS configurations
│   ├── config/                         # custom_config.xml, users.xml
│   ├── tables/                         # MergeTree DDL with codec annotations
│   ├── materialized_views/             # Incremental MV and SummingMergeTree triggers
│   └── queries/                        # Specialized vectorized functions & quantiles
│
├── druid/                              # Apache Druid event-oriented stream OLAP
│   ├── specs/                          # Native parallel ingestion specs with rollup
│   ├── supervisor/                     # Supervised Kafka stream ingestion specs
│   └── queries/                        # Timeseries and TopN Druid JSON queries
│
├── pinot/                              # Apache Pinot real-time analytical serving
│   ├── schemas/                        # Pinot dimension and metric schema definitions
│   ├── table_configs/                  # Realtime Star-Tree and inverted index configs
│   └── queries/                        # User-facing low-latency analytical serving SQL
│
├── sql-exercises/                      # 200+ Analytical SQL Exercises across 9 tiers
│   ├── 01-aggregation/                 # 30 Aggregation fundamentals
│   ├── 02-time-analytics/              # 25 Temporal resamplings and date truncations
│   ├── 03-window-functions/            # 25 Partitions, frames, running totals, and lags
│   ├── 04-top-n-ranking/               # 20 Dense ranks and top-N heap pushdowns
│   ├── 05-funnels-cohorts-retention/   # 20 Multi-stage funnels, retention matrices
│   ├── 06-joins-star-schemas/          # 20 Fact-dimension joins and star schemas
│   ├── 07-approximate-analytics/       # 20 HyperLogLog and sketch aggregations
│   ├── 08-clickhouse-sql/              # 20 ClickHouse specialized vectorized syntax
│   └── 09-physical-performance/        # 20 Query plan and projection challenges
│
├── drills/                             # 117 Query Drills across 9 categories
│   ├── aggregation/                    # 15 Grouping and measure drills
│   ├── windows/                        # 15 Window frame drills
│   ├── dates/                          # 15 Date gap-filling drills
│   ├── funnels/                        # 12 Conversion funnel drills
│   ├── cohorts/                        # 12 User cohort drills
│   ├── retention/                      # 12 Activity retention drills
│   ├── percentiles/                    # 12 SLA quantile drills
│   ├── query-plans/                    # 12 Plan operator inspection drills
│   └── optimization/                   # 12 Zone map & pushdown optimization drills
│
├── query-plans/                        # Physical execution plans with evidence
│   ├── duckdb-plans/                   # EXPLAIN ANALYZE execution profiles
│   ├── clickhouse-plans/               # EXPLAIN indexes = 1 sparse mark plans
│   └── postgres-comparison/            # EXPLAIN (BUFFERS) heap page traversals
│
├── simulations/                        # 8 First-Principles Runnable Educational Engines
│   ├── row_vs_column_sim.py            # Memory layout & byte traversal comparison
│   ├── compression_sim.py              # Dictionary, RLE, and Delta codecs from scratch
│   ├── vectorized_exec_sim.py          # Volcano tuple iterator vs 2048-row vector chunks
│   ├── zonemap_skipping_sim.py         # Min/max zone map pruning & sort order impact
│   ├── bloom_filter_sim.py             # Probabilistic data skipping from scratch
│   ├── hyperloglog_sim.py              # HLL cardinality estimation vs exact set
│   ├── tdigest_percentiles_sim.py      # Centroid clustering vs exact sort quantiles
│   └── distributed_shuffle_sim.py      # Two-phase partial aggregation vs row shuffle
│
├── broken-systems/                     # 42 Realistic Broken OLAP Debugging Labs
│   ├── lab-01-select-star-io-explosion/
│   ├── lab-02-unpartitioned-date-scan/
│   ├── lab-03-high-cardinality-partition-explosion/
│   ├── lab-04-wrong-sort-key-miss/
│   ├── lab-05-uncompressed-string-scan/
│   ├── lab-06-huge-group-by-oom/
│   ├── lab-07-exact-distinct-count-memory-spike/
│   ├── lab-08-cartesian-join-explosion/
│   ├── lab-09-hash-join-build-side-blowup/
│   ├── lab-10-tiny-insert-too-many-parts/
│   └── ... (42 labs total)
│
├── projects/                           # 10 Applied Engineering Projects
│   ├── project-01-local-parquet-analytics/
│   ├── project-02-ecommerce-star-schema/
│   ├── project-03-clickstream-funnels/
│   ├── project-04-observability-metrics/
│   ├── project-05-clickhouse-realtime-analytics/
│   ├── project-06-druid-rollup-analytics/
│   ├── project-07-analytical-api-service/
│   ├── project-08-query-benchmark-suite/
│   ├── project-09-tiny-column-store/   # Complete working binary columnar engine
│   └── project-10-tiny-vectorized-engine/ # Complete working chunk vector pipeline
│
├── capstones/                          # 7 Production Capstones
│   ├── capstone-01-build-an-olap-engine/
│   ├── capstone-02-real-time-product-analytics/
│   ├── capstone-03-observability-analytics-platform/
│   ├── capstone-04-billion-row-analytics-simulation/
│   ├── capstone-05-batch-plus-realtime-analytics/
│   ├── capstone-06-olap-production-failure-day/
│   └── final-olap-architecture-challenge/
│
├── solutions/                          # Separate Verified Solutions
│   ├── sql-exercises/                  # 200 SQL exercise solutions with plan breakdowns
│   ├── drills/                         # 117 Query drill solutions
│   └── broken-systems/                 # 42 Root cause diagnoses & architectural fixes
│
├── docs/                               # Architectural Invariant References
│   ├── glossary.md                     # Comprehensive OLAP engineering glossary
│   ├── mental-models.md                # Hardware pyramids, execution paths, shuffle maps
│   ├── analytical-query-thinking.md    # The 18 invariant analytical reasoning questions
│   ├── columnar-storage.md             # Byte layouts, Parquet anatomy, MergeTree parts
│   ├── query-execution.md              # Vectorization, SIMD, and hash aggregation
│   ├── olap-database-selection.md      # 17-dimensional comparative decision framework
│   ├── anti-patterns.md                # 17 OLAP anti-patterns with physical diagnoses
│   └── troubleshooting.md              # Diagnostic SQL queries & OOM/part remedies
│
├── phases/                             # 246 Chronological Phases (Phase 00 to Phase 245)
│   ├── 00-analytical-lab/
│   ├── 01-transactional-vs-analytical-workloads/
│   ├── ...
│   └── 245-final-olap-architecture-challenge/
│
└── outputs/                            # Persistent local database & benchmark outputs
    ├── olap_lab.duckdb
    └── tiny_col_store/
```

---

## Quickstart: Up and Running in 60 Seconds

### 1. Pre-Flight Environment Verification
```bash
make setup
make env-check
```

### 2. Launch Containerized Engines (ClickHouse & PostgreSQL)
```bash
make docker-up
```

### 3. Generate Multi-Domain Analytical Datasets (450,000+ records)
```bash
make data-small
```

### 4. Run the Full Test Suite
```bash
make test
```

### 5. Execute Format & Scan Benchmarks
```bash
make benchmark
```

---

## Measured Benchmark Evidence (No Benchmark Theater)

Running `scripts/benchmark.py` against 50,000 rows across storage formats:

```text
| Format / Storage                  |   p50 (ms) |   Mean (ms) |   p95 (ms) |   Rows Out | Speedup vs CSV |
|-----------------------------------|------------|-------------|------------|------------|----------------|
| CSV (Auto-detect row parse)       |     62.565 |      62.976 |     65.981 |          6 | 1.00x Baseline |
| Parquet (ZSTD compressed columns) |      1.021 |       1.016 |      1.074 |          6 | 61.28x faster  |
| DuckDB Native Columnar            |      1.647 |       1.688 |      1.767 |          6 | 37.92x faster  |
```

**Why Columnar Storage Wins**:
1. **Projection Pushdown**: In Parquet, only the 2 referenced columns (`country`, `net_revenue`) were read from storage. The remaining 12 columns were never loaded or decompressed.
2. **Binary SIMD Decoding**: Values were loaded directly into CPU vector registers without ASCII-to-float string parsing.

---

## The Completion Standard

The learner is finished when:

```text
"This analytical query is slow."
```

does **NOT** immediately cause:

```text
add more hardware
add an index
```

Instead they think:

```text
What is the input grain?
How much data?
Which columns?
Which partitions?
How many bytes?
What is the filter selectivity?
What data can be skipped?
Is the storage ordered correctly?
What is GROUP BY cardinality?
Is a sort required?
Is there a join?
How big are both sides?
Is there shuffle?
Can we preaggregate?
Can approximate computation work?
Is the workload concurrency-bound?
Is this even the right database?
```

And they can trace the complete physical query path from memory to disk:

```text
SQL
 ↓
parser
 ↓
logical plan
 ↓
optimizer
 ↓
physical plan
 ↓
partition pruning
 ↓
column scan
 ↓
block/segment skipping
 ↓
decompression
 ↓
vectorized operators
 ↓
partial aggregation
 ↓
distributed merge if needed
 ↓
final rows
```
