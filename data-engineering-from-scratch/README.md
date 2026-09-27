# Data Engineering From Scratch

> **Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.**

---

```text
                                 DATA ENGINEERING FROM SCRATCH
                                               
                                            Records
                                               ↓
                                            Schemas
                                               ↓
                                             Files
                                               ↓
                                             Batch
                                               ↓
                                           Ingestion
                                               ↓
                                      SQL Transformations
                                               ↓
                                           Warehouse
                                               ↓
                                         Data Modeling
                                               ↓
                                         Partitioning
                                               ↓
                                         Orchestration
                                               ↓
                                            Quality
                                               ↓
                                              CDC
                                               ↓
                                           Streaming
                                               ↓
                                        Lake / Lakehouse
                                               ↓
                                            Lineage
                                               ↓
                                         Observability
                                               ↓
                                         Data Platform
```

---

## 1. What This Repository Is

This is **NOT** an Airflow tutorial.

This is **NOT** a Spark certification guide.

This is **NOT** a dbt cheatsheet or a cloud vendor marketing manual.

**This is a course in engineering trustworthy data systems.**

In modern software development, data engineering is frequently mischaracterized as knowing how to configure a specific set of tools: *"We need data engineering, so let's install Airflow, Spark, Kafka, and Snowflake."*

This repository exists to deconstruct that illusion.

Tools change every five years. The underlying physics of moving, validating, organizing, and recovering data remain invariant:
- **I/O & Storage Physics**: Why row-oriented pages fail on analytical rollups and how columnar formats (Parquet) save 75% disk space and 40x scan I/O.
- **Relational Invariants & Grain**: What exactly does one row represent? How does an un-idempotent join or retry silently duplicate revenue metrics by 200%?
- **Failure & Recovery**: What happens when a network drops at byte 5,000,000 of a 10 GB file? Does the pipeline expose dirty reads, or commit atomically?
- **Temporal Mechanics**: Event time vs processing time, watermarks, late-arriving data, and tumbling window aggregations.
- **Producer-Consumer Contracts**: How to evolve data contracts without taking down downstream analytics dashboards.

The target mental model is:

> **Data Engineering is the discipline of moving, transforming, validating, organizing, and operating data so that downstream systems can depend on it.**

---

## 2. Core Curriculum Highlights

An exhaustive, 20-part syllabus spanning **201 Phases (Phase 00 through Phase 200)**, accompanied by:
- **32 Realistic Broken-Pipeline Incident Labs** (`broken-pipelines/`) covering silent duplication, memory exhaustion, schema drift, watermarks, and CDC offset loss.
- **17 Substantial Applied Projects** (`projects/`) implementing real-world ingestion, warehousing, lakehouses, orchestration, and streaming engines.
- **185 Practical Exercises** (`exercises/`) across 13 core domains with separate reference solutions.
- **6 Capstone Platforms** (`phases/192` to `phases/197`) synthesizing batch, real-time, CDC, lakehouse, and observability architectures.
- **435 Automated Test Suites** passing across all modules with zero dependencies outside standard Python, DuckDB, and PyArrow.

---

## 3. The 12-Step Learning Methodology

Every phase and lesson in this repository adheres strictly to the first-principles learning cycle:

```text
MOTTO ──> PROBLEM ──> PREDICT ──> FIRST PRINCIPLES ──> MENTAL MODEL ──> BUILD SIMPLE VERSION
  │
  └───> RUN IT ──> INSPECT ──> VALIDATE ──> MEASURE ──> BREAK ──> RECOVER ──> REPLAY ──> EVIDENCE
```

1. **Problem First**: State the concrete bottleneck, corruption, or failure mode without mentioning third-party vendor tools.
2. **Predict**: Hypothesize row counts, byte volumes, and failure modes before executing code.
3. **Build the Simple Version**: Implement the core primitive in pure Python or standard ANSI SQL.
4. **Inspect Intermediate State**: Examine staging files, checkpoint files, and temporary buffers.
5. **Validate Output**: Assert primary key uniqueness, nullability, and value domain constraints.
6. **Measure**: Benchmark rows/sec, MB/sec, memory RSS, and query execution plans.
7. **Break It Deliberately**: Inject poisoned data, kill processes mid-flight, and simulate duplicates.
8. **Recover & Replay**: Quarantine corrupt records, execute atomic partition replacements, and verify idempotency ($f(f(x)) = f(x)$).
9. **Log Evidence**: Fill out the empirical evidence record in `outputs/evidence-template.md`.

---

## 4. Repository Quickstart

### Prerequisites
- Python 3.11 or higher
- Bash or Zsh shell
- Docker (optional, for local PostgreSQL and MinIO containers)

### Setup in 3 Commands

```bash
# 1. Clone repository
git clone https://github.com/rohitg00/data-engineering-from-scratch.git
cd data-engineering-from-scratch

# 2. Set up virtual environment and install core packages (DuckDB, PyArrow, Pytest)
make setup

# 3. Verify environment and generate sample datasets
make check-env
make generate-data
```

### Running the Test Suites

```bash
# Run all 435 tests across phases, projects, broken pipelines, and exercises
make test

# Run tests for specific sections
make test-phases      # 201 phases
make test-projects    # 17 projects
make test-broken      # 32 broken-pipeline scenarios
make test-exercises   # 185 practical exercises
```

---

## 5. Repository Directory Layout

```text
data-engineering-from-scratch/
├── README.md                      # Repository overview and philosophy
├── ROADMAP.md                     # Exhaustive 201-phase curriculum syllabus
├── LEARNING.md                    # Core principles & 15 rules of data engineering
├── LESSON_TEMPLATE.md             # Standardized 20-section lesson template
├── VERSIONS.md                    # Tested tool versions and compatibility matrix
├── DATA_CONTRACTS.md              # Producer-consumer contract specification
├── CONTRIBUTING.md                # Contribution guidelines and coding standards
├── Makefile                       # Operational automation targets
├── pyproject.toml                 # Package configuration and pytest settings
├── requirements.txt               # Pinned Python dependencies
├── docker-compose.yml             # Local PostgreSQL and MinIO services
│
├── scripts/
│   ├── check-environment.sh       # Environment verification script
│   ├── generate-data.py           # Synthetic dataset generator (CSV, JSON, Parquet)
│   ├── reset-lab.sh               # Lab cleanup and dataset refresh
│   └── validate-data.py           # Ingestion contract validation utility
│
├── docs/
│   ├── glossary.md                # Comprehensive data engineering terminology
│   ├── mental-models.md           # Core conceptual models & storage physics
│   ├── pipeline-design.md         # The 19 core pipeline design invariants
│   ├── data-quality.md            # The 6 data quality dimensions & quarantine
│   ├── lineage.md                 # Upstream/downstream provenance graphs
│   └── troubleshooting.md         # Production incident triage and playbooks
│
├── datasets/
│   ├── raw/                       # Clean source datasets (orders, users, clicks, CDC)
│   ├── corrupted/                 # Intentionally corrupted test files
│   └── partitioned/               # Hive-partitioned Parquet datasets
│
├── pipelines/
│   ├── batch_ingestion.py         # Production batch ingestion with quarantine
│   ├── incremental_cdc.py         # Incremental CDC stream replication & offsets
│   ├── streaming_window_aggregator.py # Tumbling window aggregator with watermarks
│   ├── idempotent_upsert.py       # Idempotent merge/upsert demonstration
│   └── backfill_coordinator.py   # Historical date partition backfill engine
│
├── transformations/
│   ├── staging/                   # Cleaned, normalized staging SQL models
│   ├── intermediate/              # Multi-table join and aggregate SQL models
│   └── marts/                     # Consumer-facing dimensional marts SQL
│
├── schemas/
│   ├── init.sql                   # Transactional OLTP database schema (DDL)
│   ├── dimensional/               # Kimball star schema DDL (dim_*, fact_*)
│   └── contracts/                 # Executable JSON schema contracts
│
├── benchmarks/
│   ├── benchmark_csv_vs_parquet.py # Compression and column pruning benchmarks
│   ├── benchmark_partition_pruning.py # Partition filter speedup measurements
│   └── benchmark_small_files_compaction.py # Small files overhead vs compaction
│
├── broken-pipelines/              # 32 Realistic data-pipeline failure scenarios
│   ├── lab-01-missing-delimiter-malformed-csv/
│   ├── lab-02-silent-type-coercion-string-to-int/
│   ├── ... (32 separate labs with broken code, solutions, and tests)
│   └── lab-32-corrupted-parquet-footer-dictionary-crash/
│
├── projects/                      # 17 Substantial end-to-end applied projects
│   ├── 01-ecommerce-batch-pipeline/
│   ├── 02-clickstream-pipeline/
│   ├── 03-cdc-pipeline/
│   ├── 04-data-lake/
│   ├── 05-lakehouse-table-format/
│   ├── 06-data-warehouse-star-schema/
│   ├── ... (17 complete projects with code and tests)
│   └── 17-data-catalog-lite/
│
├── exercises/                     # 185 Practical exercises across 13 domains
│   ├── 01-files-and-formats/
│   ├── 02-ingestion/
│   ├── 03-sql-modeling/
│   ├── 04-warehousing/
│   ├── 05-dbt-transformations/
│   ├── 06-orchestration/
│   ├── 07-partitioning-and-storage/
│   ├── 08-distributed-spark/
│   ├── 09-cdc-replication/
│   ├── 10-streaming-systems/
│   ├── 11-data-quality-and-contracts/
│   ├── 12-lineage-and-metadata/
│   └── 13-performance-and-debugging/
│
├── phases/                        # 201 Phases (Phase 00 through Phase 200)
│   ├── 00-data-engineering-lab/
│   ├── 01-what-is-data-engineering/
│   ├── ...
│   └── 200-final-design-challenge/
│
└── outputs/
    └── evidence-template.md       # Standardized evidence log template
```

---

## 6. How This Course Connects to the Software Engineering Discipline

- **Connection to SQL**: SQL is treated as a compiled, declarative relational algebra language, not just an ad-hoc query syntax. You write CTEs, window functions, and surrogate key lookups with full awareness of query plan execution.
- **Connection to Kafka & Streaming**: We deconstruct append-only logs, consumer group offsets, high-watermarks, and late data before ever launching a broker daemon.
- **Connection to Backend Engineering**: We define the operational boundaries between primary transactional databases and analytical replicas. You will learn how unindexed ETL queries lock production databases, and how Transactional Outbox and CDC decouple application state.
- **Connection to Cloud & AWS**: Cloud storage (S3), compute clusters (EMR), and serverless query engines (Athena) are evaluated as cost-per-scan and network egress primitives. You learn to minimize scans through Parquet column pruning and partition pruning before paying cloud provider bills.
- **Connection to System Design**: Data engineering is the persistence, movement, and analytical dimension of distributed systems design. It answers how massive state moves across nodes deterministically under partial network and hardware failure.

---

> Data Engineering is no longer a collection of pipeline tools.
>
> We started with raw records and files, learned how schemas protect meaning, built repeatable ingestion and transformation pipelines, modeled analytical data, partitioned and compressed large datasets, orchestrated dependencies, captured database changes, processed streams, validated data quality, and operated pipelines under failure.
>
> Now when data must move from one system to another, we can reason about freshness, correctness, replayability, schema evolution, idempotency, lineage, cost, and failure before choosing the technology that implements the pipeline.
