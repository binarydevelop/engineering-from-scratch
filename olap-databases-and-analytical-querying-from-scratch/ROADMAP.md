# Curriculum Roadmap: 32 Parts, 246 Phases

> **Motto**: Understand it. Model it. Query it. Scan it. Aggregate it. Measure it. Break it. Optimize it. Scale it.

---

## High-Level Curriculum Progression

```text
Analytical Questions
       ↓
Analytical SQL Fluency
       ↓
Row vs Column Physical Layout
       ↓
Compression & Specialized Codecs
       ↓
Vectorized Execution & SIMD
       ↓
Parquet Storage & Pushdowns
       ↓
Data Skipping & Zone Maps
       ↓
Partitioning Mechanics
       ↓
Query Planning & Cost Estimation
       ↓
Analytical Joins & Star Schemas
       ↓
Advanced Aggregations & Sketches
       ↓
DuckDB In-Process Engine
       ↓
ClickHouse MergeTree & Production OLAP
       ↓
Materialization & Incremental Views
       ↓
Real-Time OLAP & Streaming
       ↓
Apache Druid & Segment Rollup
       ↓
Apache Pinot & Low-Latency Serving
       ↓
Distributed OLAP & Network Shuffle
       ↓
Query Concurrency & Governance
       ↓
Real-Time Analytical Patterns
       ↓
High-Cardinality Engineering
       ↓
Time-Series Analytical Design
       ↓
Analytical Data Modeling
       ↓
Data Quality & Reconciliation
       ↓
Performance Engineering & Profiling
       ↓
High-Throughput Ingestion
       ↓
Failure Modes & Production Triage
       ↓
OLAP Database Selection Framework
       ↓
Cross-Database Comparative Querying
       ↓
Query Mastery & Plan Reasoning
       ↓
Educational Projects & Engines
       ↓
Production Capstones
```

---

## Detailed Manifest of Parts and Phases

### PART I — WHY OLAP EXISTS (Phases 00–06)
- **Phase 00**: Analytical Laboratory Setup (DuckDB, Postgres, ClickHouse, Synthetic Data)
- **Phase 01**: Transactional vs Analytical Workloads (Point Reads vs Column Scans)
- **Phase 02**: OLTP vs OLAP Mental Model (Heap Pages vs Columnar Arrays)
- **Phase 03**: Formulating Analytical Questions (Revenue, Retention, Latency)
- **Phase 04**: Data Grain: The Non-Negotiable Contract of Analytical Modeling
- **Phase 05**: Dimensions and Measures (Context vs Quantifiable Facts)
- **Phase 06**: Slice, Dice, Roll-Up, and Drill-Down via Modern SQL

### PART II — ANALYTICAL SQL FLUENCY (Phases 07–20)
- **Phase 07**: GROUP BY Execution Deeply (Keys -> States -> Results)
- **Phase 08**: Aggregations & Three-Valued NULL Semantics
- **Phase 09**: Conditional Aggregation for Dashboard Pivots (CASE in Aggregates)
- **Phase 10**: High-Cardinality DISTINCT Workloads & Memory Bounds
- **Phase 11**: Approximate Distinct Counting & HyperLogLog
- **Phase 12**: Quantiles & Percentiles (p50, p90, p95, p99 Tail Latencies)
- **Phase 13**: Temporal Bucketing and Continuous Resampling (`date_trunc`)
- **Phase 14**: Window Functions Fundamentals (Frames, Partitions, Running Totals)
- **Phase 15**: Top-N Ranking per Analytical Partition (`DENSE_RANK`, `QUALIFY`)
- **Phase 16**: Conversion Funnels Analysis (Multi-Stage Drop-Offs)
- **Phase 17**: Cohort Analysis (Acquisition vs Retention Matrices)
- **Phase 18**: N-Day Activity Retention Curves (Day-1, Day-7, Day-30)
- **Phase 19**: Clickstream Sessionization using Inactivity Time Gaps
- **Phase 20**: Analytical SQL Mastery Challenge Set I (30 Complex Problems)

### PART III — ROW VS COLUMN STORAGE (Phases 21–29)
- **Phase 21**: Build a Tiny Row Store from Scratch (Array of Structs)
- **Phase 22**: Build a Tiny Column Store from Scratch (Struct of Arrays)
- **Phase 23**: Column Projection Pushdown Mechanics
- **Phase 24**: Why Column Stores Compress 10x Better (Information Entropy)
- **Phase 25**: Dictionary Encoding from First Principles
- **Phase 26**: Run-Length Encoding (RLE) on Sorted Columns
- **Phase 27**: Delta Encoding for Monotonic Sequences
- **Phase 28**: Bit Packing & Frame of Reference (FoR)
- **Phase 29**: Compression Tradeoffs: CPU Decompression vs Disk Bandwidth

### PART IV — VECTORISED EXECUTION (Phases 30–35)
- **Phase 30**: Row-at-a-Time Volcano Iterator Overhead
- **Phase 31**: Batch Chunk Processing in L1/L2 Caches (2,048 Rows)
- **Phase 32**: Vectorized Execution: Column Vectors to Operators
- **Phase 33**: SIMD Hardware Acceleration & Register Widths (AVX2, Neon)
- **Phase 34**: Branch Reduction & Selection Vectors
- **Phase 35**: Inspecting Vector Execution in DuckDB Plans

### PART V — FILE FORMATS (Phases 36–43)
- **Phase 36**: CSV vs Parquet: Deep Physical Benchmark
- **Phase 37**: Parquet Row Groups: Horizontal Partitioning
- **Phase 38**: Column Chunks & Data Pages Layout
- **Phase 39**: Parquet Page Statistics & Zone Map Pruning
- **Phase 40**: Predicate Pushdown into Parquet Readers
- **Phase 41**: Projection Pushdown into Parquet Readers
- **Phase 42**: The Small Files Problem in Analytical Lakes
- **Phase 43**: Compaction Algorithms & Batch Merging

### PART VI — DATA SKIPPING (Phases 44–49)
- **Phase 44**: Full Table Scan Baseline & I/O Bounds
- **Phase 45**: Zone Maps (Min/Max Skipping) from Scratch
- **Phase 46**: Sparse Indexes vs Dense B-Trees
- **Phase 47**: Bloom Filter Indexes for Equality Pruning
- **Phase 48**: How Sort Order Dictates Pruning Efficiency
- **Phase 49**: Choosing the Optimal Sorting Key Hierarchy

### PART VII — PARTITIONING (Phases 50–55)
- **Phase 50**: Temporal Partitioning by Date and Month
- **Phase 51**: Failure Mode: Too Few Massive Partitions
- **Phase 52**: Failure Mode: Partition Explosion & Inode Exhaustion
- **Phase 53**: High-Cardinality Partition Anti-Pattern
- **Phase 54**: Verifying Partition Pruning via Physical Plans
- **Phase 55**: Partitioning vs Sorting: The Critical Distinction

### PART VIII — QUERY ENGINES (Phases 56–64)
- **Phase 56**: SQL Parsing & Abstract Syntax Trees (AST)
- **Phase 57**: Logical Plans: Operators and Relational Algebra
- **Phase 58**: Physical Plan Generation & Operator Assignment
- **Phase 59**: Cost-Based Optimization & Cardinality Estimation
- **Phase 60**: Optimizer Rule: Filter Pushdown to Storage
- **Phase 61**: Optimizer Rule: Early Projection Elimination
- **Phase 62**: Join Reordering & Intermediate State Minimization
- **Phase 63**: Two-Phase Partial Aggregation Mechanics
- **Phase 64**: Push-Based Pipelined Execution Engines

### PART IX — ANALYTICAL JOINS (Phases 65–71)
- **Phase 65**: Fact Table + Dimension Joins
- **Phase 66**: Star Schema Design for Query Acceleration
- **Phase 67**: Hash Join from First Principles (Build + Probe)
- **Phase 68**: Broadcast Joins for Asymmetric Relations
- **Phase 69**: Partitioned / Shuffle Hash Joins
- **Phase 70**: Cartesian Products & Join Explosions
- **Phase 71**: Denormalization: Wide Tables vs Star Joins

### PART X — ADVANCED AGGREGATIONS (Phases 72–76)
- **Phase 72**: HyperLogLog Implementation from Scratch
- **Phase 73**: Exact vs Approximate Distinct Counting Benchmark
- **Phase 74**: Approximate Quantiles with t-Digest / DDSketch
- **Phase 75**: Top-K Heavy Hitters (Count-Min Sketch)
- **Phase 76**: When and Why Approximate Analytics Wins

### PART XI — DUCKDB (Phases 77–84)
- **Phase 77**: DuckDB: The In-Process Vectorized Analytical Engine
- **Phase 78**: Direct Zero-Ingest CSV Querying
- **Phase 79**: Direct Parquet Querying with Full Pushdown
- **Phase 80**: DuckDB Native Storage (.duckdb) & Buffer Manager
- **Phase 81**: Deep Plan Inspection with EXPLAIN ANALYZE
- **Phase 82**: Querying Lists, Structs, and Maps in DuckDB
- **Phase 83**: Large-Scale Local Aggregation Benchmark
- **Phase 84**: DuckDB vs PostgreSQL: Fair Workload Comparison

### PART XII — CLICKHOUSE FOUNDATIONS (Phases 85–96)
- **Phase 85**: Why ClickHouse? Columnar DBMS Architecture
- **Phase 86**: ClickHouse Execution Pipeline & Parts Lifecycle
- **Phase 87**: Creating MergeTree Tables: Engines and Settings
- **Phase 88**: High-Throughput Batch Ingestion Mechanics
- **Phase 89**: Querying Columnar Data: Profiling and Plans
- **Phase 90**: MergeTree Parts, Immutability, and Background Merges
- **Phase 91**: ClickHouse Primary vs Sorting Key (ORDER BY)
- **Phase 92**: Designing Workload-Centric Sorting Keys
- **Phase 93**: Granules, Marks (.mrk2), and Sparse Indexing
- **Phase 94**: Data Skipping Indexes: MinMax, Set, Bloom Filter
- **Phase 95**: Partition Pruning in ClickHouse (PARTITION BY)
- **Phase 96**: Compression Codecs: LZ4, ZSTD, Delta, T64, Gorilla

### PART XIII — CLICKHOUSE DATA MODELING (Phases 97–103)
- **Phase 97**: Append-Only Event Tables at Massive Scale
- **Phase 98**: Denormalized Wide Tables in ClickHouse
- **Phase 99**: Arrays, Tuples, and Nested Data Structures
- **Phase 100**: LowCardinality String Optimization
- **Phase 101**: ReplacingMergeTree & Versioned Record Deduplication
- **Phase 102**: Deduplication: Eventual Merges vs FINAL Keyword
- **Phase 103**: Mutations: Lightweight Deletes and ALTER UPDATE

### PART XIV — MATERIALIZATION (Phases 104–110)
- **Phase 104**: The Economics of Precomputation vs Raw Scans
- **Phase 105**: Building Incremental Materialized Views from Scratch
- **Phase 106**: ClickHouse Incremental Materialized Views (TO table)
- **Phase 107**: Mergeable Aggregate States (AggregateFunction)
- **Phase 108**: Projections: Multi-Layout Physical Tables
- **Phase 109**: Raw Event Granularity vs Pre-Aggregated Rollups
- **Phase 110**: Hourly and Daily Hierarchical Rollups

### PART XV — REAL-TIME OLAP (Phases 111–116)
- **Phase 111**: Batch Latency vs Real-Time Freshness Tradeoffs
- **Phase 112**: Streaming Ingestion: Kafka to Columnar Engines
- **Phase 113**: Measuring End-to-End Event Freshness
- **Phase 114**: Handling Late-Arriving Events & Out-of-Order Data
- **Phase 115**: Real-Time Upserts vs Append-Only Logs
- **Phase 116**: Event-Time vs Ingestion-Time Partitioning

### PART XVI — APACHE DRUID (Phases 117–127)
- **Phase 117**: Apache Druid Architecture & Cluster Roles
- **Phase 118**: Druid Datasources: Relational Tables for Time-Series
- **Phase 119**: Data Modeling: Timestamps, Dimensions, and Metrics
- **Phase 120**: Immutable Columnar Segments & Deep Storage
- **Phase 121**: Time Chunking & Segment Pruning Mechanics
- **Phase 122**: Ingestion-Time Rollup: Compacting Event Streams
- **Phase 123**: Bitmap Indexes for High-Speed Categorical Filtering
- **Phase 124**: Batch Ingestion via Native Indexing Tasks
- **Phase 125**: Supervised Kafka Streaming Ingestion
- **Phase 126**: Broker Scatter-Gather Query Routing & Result Merges
- **Phase 127**: Executing Analytical SQL over Druid Datasources

### PART XVII — APACHE PINOT (Phases 128–133)
- **Phase 128**: Apache Pinot: Ultra-Low Latency Analytical Serving
- **Phase 129**: Pinot Architecture: Controllers, Brokers, and Servers
- **Phase 130**: Pinot Columnar Segments and Forward/Inverted Indexes
- **Phase 131**: Offline vs Realtime Table Pairs & Segment Completion
- **Phase 132**: Specialized Indexes: Star-Tree, Range, Text, Json
- **Phase 133**: User-Facing Sub-50ms Query Serving

### PART XVIII — DISTRIBUTED OLAP (Phases 134–144)
- **Phase 134**: When Single-Node Scaling Reaches Hardware Limits
- **Phase 135**: Data Sharding: Hash, Range, and Random Distribution
- **Phase 136**: Parallel Distributed Scans Across Worker Nodes
- **Phase 137**: Distributed Partial Aggregation & Coordinator Merge
- **Phase 138**: Distributed GROUP BY with High Distinct Cardinality
- **Phase 139**: Distributed Sorting & Global Top-N Merging
- **Phase 140**: The Network Shuffle Bottleneck in Distributed Queries
- **Phase 141**: Distributed Joins: Colocated vs Broadcast vs Shuffle
- **Phase 142**: The Query Coordinator: Query Planning & Task Dispatch
- **Phase 143**: The Straggler Effect: Diagnosing the Slowest Worker
- **Phase 144**: Replication for Availability vs Partitioning for Scale

### PART XIX — QUERY CONCURRENCY (Phases 145–151)
- **Phase 145**: Resource Consumption of a Single Massive Scan
- **Phase 146**: Resource Contention under 100 Concurrent Queries
- **Phase 147**: Admission Control, Queuing, and Query Rejection
- **Phase 148**: Query Memory Governance & Disk Spilling Thresholds
- **Phase 149**: Workload Classes: Separating BI from Batch Pipelines
- **Phase 150**: Query Timeouts & Killing Runaway Scans
- **Phase 151**: CPU and Thread Pool Governance Policies

### PART XX — REAL-TIME ANALYTICS PATTERNS (Phases 152–157)
- **Phase 152**: Observability Analytics: High-Volume Logs and Spans
- **Phase 153**: Product Analytics: Event Streams, Funnels, and Cohorts
- **Phase 154**: Ad Tech Analytics: High-Throughput Impressions & Spend
- **Phase 155**: IoT Telemetry Analytics: High-Frequency Sensor Timeseries
- **Phase 156**: Financial Reporting Analytics: Exact Reconciliation
- **Phase 157**: Security Analytics: Anomaly Detection Across Audit Logs

### PART XXI — HIGH CARDINALITY (Phases 158–162)
- **Phase 158**: Understanding Cardinality: Low vs High vs Extreme
- **Phase 159**: GROUP BY High-Cardinality Memory Exhaustion
- **Phase 160**: DISTINCT High-Cardinality Performance Degradation
- **Phase 161**: Filtering on High-Cardinality Keys: Index Implications
- **Phase 162**: Preventing Dimensional Cardinality Explosion

### PART XXII — TIME-SERIES ANALYTICS (Phases 163–167)
- **Phase 163**: Time as the Primary Analytical Dimension
- **Phase 164**: Optimizing Time-Range Queries via Physical Layout
- **Phase 165**: Downsampling: Transforming 1-Second Data into 1-Hour Summaries
- **Phase 166**: Tiered Retention: Hot NVMe vs Warm Parquet vs Cold S3
- **Phase 167**: Automated Partition Expiry with TTLs

### PART XXIII — DATA MODELING (Phases 168–174)
- **Phase 168**: Star Schema Revisited: Foreign Keys & Dimensional Integrity
- **Phase 169**: Wide Table Denormalization in Modern Column Stores
- **Phase 170**: Slowly Changing Dimensions (Type 2 SCD in OLAP)
- **Phase 171**: Handling Late-Arriving Dimension Keys
- **Phase 172**: Snapshot Fact Tables: Capturing Point-in-Time State
- **Phase 173**: Event Fact Tables: Modeling Immutable Occurrences
- **Phase 174**: Aggregate Fact Tables: Precomputing Complex Metrics

### PART XXIV — ANALYTICAL DATA QUALITY (Phases 175–180)
- **Phase 175**: Correct Query, Wrong Data: The Duplicate Pipeline Pathology
- **Phase 176**: Deduplicating Events across Distributed Streams
- **Phase 177**: Detecting Missing Data & Volume Anomalies
- **Phase 178**: Handling Late Data Restatements & Historical Edits
- **Phase 179**: Reconciliation: Source of Truth vs OLAP Aggregate Parity
- **Phase 180**: Tracking Ingestion Lag & Metric Freshness

### PART XXV — PERFORMANCE ENGINEERING (Phases 181–192)
- **Phase 181**: Rigorous Benchmark Methodology & Control Variables
- **Phase 182**: Cold Cache vs Warm Cache: Unmasking Memory Traps
- **Phase 183**: Measuring Physical Bytes Scanned vs Logical Tuples
- **Phase 184**: Tracking Rows Filtered vs Rows Returned
- **Phase 185**: Profiling CPU Instructions and SIMD Vectorization
- **Phase 186**: Measuring Query Peak Memory & Spill Overhead
- **Phase 187**: Calculating Empirical Compression Ratios Across Codecs
- **Phase 188**: Using Database Execution Profilers (query_log, EXPLAIN)
- **Phase 189**: Case Study: Optimizing a Selective Filter Query (10x Gain)
- **Phase 190**: Case Study: Optimizing a Massive GROUP BY Aggregation
- **Phase 191**: Case Study: Optimizing Large Fact + Dimension Joins
- **Phase 192**: Case Study: Accelerating a 10-Query Dashboard (100x Gain)

### PART XXVI — INGESTION (Phases 193–200)
- **Phase 193**: Single-Row Inserts: Measuring Write Amplification
- **Phase 194**: Batch Inserts: Finding the Optimal Chunk Size (50k-100k)
- **Phase 195**: Bulk File Ingestion: Streaming Parquet and CSV
- **Phase 196**: Streaming Ingestion: Kafka Consumer Architecture
- **Phase 197**: Measuring Ingestion Throughput: Rows/sec & MB/sec
- **Phase 198**: Ingestion vs Query Resource Competition & CPU Throttling
- **Phase 199**: Backpressure: What Happens When Producers Outrun Ingestion
- **Phase 200**: Safe Historical Data Replays and Backfills

### PART XXVII — FAILURE MODES (Phases 201–212)
- **Phase 201**: ClickHouse Failure: Too Many Parts in MergeTree
- **Phase 202**: Failure Mode: Poor Sort Key Causing Full Scans
- **Phase 203**: Failure Mode: Unpruned or Oversharded Partitions
- **Phase 204**: Failure Mode: High-Cardinality GROUP BY OOM
- **Phase 205**: Failure Mode: Many-to-Many Join Explosion
- **Phase 206**: Failure Mode: Treating Columnar Engines Like OLTP
- **Phase 207**: Failure Mode: Shard Data Skew and Hot-Spotting
- **Phase 208**: Failure Mode: Background Merge Backlog & Part Stall
- **Phase 209**: Failure Mode: Distributed Replica Desynchronization
- **Phase 210**: Failure Mode: Storage Exhaustion & Read-Only Locks
- **Phase 211**: Failure Mode: The Dashboard Refresh Query Storm
- **Phase 212**: The Broken OLAP Lab Suite: 42 Diagnostic Labs

### PART XXVIII — OLAP DATABASE SELECTION (Phases 213–220)
- **Phase 213**: DuckDB Fits When: In-Process, Embedded, Parquet Lake
- **Phase 214**: ClickHouse Fits When: Billion-Row Events, Real-Time Ingest
- **Phase 215**: Apache Druid Fits When: Stream Rollup, Event Analytics
- **Phase 216**: Apache Pinot Fits When: Sub-50ms User-Facing SLAs
- **Phase 217**: Cloud Warehouses Fit When: BigQuery, Snowflake, Redshift
- **Phase 218**: PostgreSQL Fits When: Analytics Under 20 GB (Mandatory Lesson)
- **Phase 219**: Why Elasticsearch/OpenSearch is Not General OLAP
- **Phase 220**: Time-Series Databases (Timescale/Influx) vs Columnar OLAP

### PART XXIX — CROSS-DATABASE QUERYING (Phases 221–224)
- **Phase 221**: Executing the Same Query in PostgreSQL and DuckDB
- **Phase 222**: Executing the Same Query in DuckDB and ClickHouse
- **Phase 223**: Same Dashboard Workload: Raw Scan vs Materialized View
- **Phase 224**: Same Event Workload in ClickHouse and Apache Druid

### PART XXX — QUERY MASTERY (Phases 225–228)
- **Phase 225**: Analytical Query Mastery Challenge I (40 Queries)
- **Phase 226**: Analytical Query Mastery Challenge II (50 Harder Queries)
- **Phase 227**: Performance Query Challenge: Given Slow Query, Optimize Plan
- **Phase 228**: Physical Query Reasoning: Predict Plan Before Running

### PART XXXI — PROJECTS (Phases 229–238)
- **Phase 229**: Project: 100M-Row Local Parquet Engine with DuckDB
- **Phase 230**: Project: E-Commerce Star Schema & Customer LTV Analytics
- **Phase 231**: Project: Real-Time Clickstream Funnels & Sessionization
- **Phase 232**: Project: Observability Platform: Log Traces & Tail Latencies
- **Phase 233**: Project: ClickHouse Real-Time Serving Architecture
- **Phase 234**: Project: Apache Druid Stream Ingestion & Rollup Serving
- **Phase 235**: Project: Production Analytical API with Concurrency Governance
- **Phase 236**: Project: Multi-Engine Query Benchmark Suite
- **Phase 237**: Project: Tiny Column Store: Binary Storage & Zone Maps
- **Phase 238**: Project: Tiny Vectorized Engine: Chunk Execution & SIMD

### PART XXXII — CAPSTONES (Phases 239–245)
- **Phase 239**: Capstone 1: Build an Educational OLAP Engine from Scratch
- **Phase 240**: Capstone 2: Real-Time Product Analytics Platform
- **Phase 241**: Capstone 3: Observability Analytics Platform
- **Phase 242**: Capstone 4: Scalable Analytical Stress Simulation
- **Phase 243**: Capstone 5: Unified Batch + Real-Time Analytics
- **Phase 244**: Capstone 6: OLAP Production Chaos & Failure Day
- **Phase 245**: Final Capstone: 5 TB/Day Global SaaS Analytics Architecture
