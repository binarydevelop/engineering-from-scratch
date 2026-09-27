# NoSQL Databases & Query Languages From Scratch

> **Motto:** Understand it. Model it. Query it. Partition it. Measure it. Break it. Recover it. Scale it.

```text
This is NOT a MongoDB tutorial.

This is NOT a Cassandra tutorial.

This is NOT a list of NoSQL commands.

This is a course in NoSQL data modeling,
query-language fluency,
and distributed database reasoning.
```

---

## 1. The Core Philosophy

In software engineering education, NoSQL is too often taught as either a grab-bag of command-line syntaxes or reduced to the false slogan that *"NoSQL scales better than SQL."*

Both views are wrong.

```text
NoSQL ≠ one database category
NoSQL ≠ no query language
NoSQL ≠ faster than SQL
```

NoSQL systems comprise fundamentally different physical and logical data models:
* **Document Databases** (Hierarchical BSON / WiredTiger B-Trees)
* **Wide-Column Stores** (LSM Trees, SSTables, Commit Logs, Partition Rings)
* **Key-Value Stores** (Distributed Hash Tables, B-Tree Partitions)
* **In-Memory Structured Stores** (RAM-Resident Hash Tables, SkipLists, Radix Trees)
* **Native Property Graphs** (Index-Free Adjacency, Pointer-Chained Edges)
* **Search Engines** (Inverted Indexes, Lucene Segment Postings)

The central discipline of this curriculum is:

```text
business requirement
       ↓
access pattern
       ↓
data shape
       ↓
data model
       ↓
key / partition design
       ↓
query language
       ↓
index
       ↓
physical execution
       ↓
distributed behavior
       ↓
performance
       ↓
failure behavior
```

The learner will finish this course able to answer both:
1. **How do I query this database?**
2. **Why does this database require me to query it this way?**

---

## 2. Two Parallel Tracks

This curriculum advances two tracks simultaneously and merges them:

```text
┌──────────────────────────────────────────────┐    ┌──────────────────────────────────────────────┐
│  TRACK A: NoSQL Query Languages              │    │  TRACK B: NoSQL Database Engineering         │
├──────────────────────────────────────────────┤    ├──────────────────────────────────────────────┤
│  • Key point lookups                         │    │  • Hash tables & in-memory stores            │
│  • Document queries & filter expressions     │    │  • BSON encoding & document boundaries       │
│  • Array querying & $elemMatch               │    │  • LSM Trees: Memtable, Commit Log, SSTable  │
│  • In-place update operators                 │    │  • Bloom filters, tombstones & compaction    │
│  • Multi-stage aggregation pipelines         │    │  • Hash partitioning vs Consistent Hashing   │
│  • CQL partition & clustering key queries    │    │  • Token rings & virtual nodes               │
│  • DynamoDB KeyConditions vs Scans           │    │  • Replication factor & quorum math (N, R, W)│
│  • PartiQL SQL-compatible expressions        │    │  • Stale reads, read repair & hinted handoff │
│  • Cypher graph pattern matching             │    │  • PACELC / CAP theorem under real partitions│
│  • Elasticsearch JSON Query DSL              │    │  • Read, write & network amplification       │
│  • Distributed query reasoning & fan-out     │    │  • Distributed failure recovery & rebalancing│
└──────────────────────┬───────────────────────┘    └──────────────────────┬───────────────────────┘
                       │                                                   │
                       └─────────────────────────┬─────────────────────────┘
                                                 ▼
                              ┌─────────────────────────────────────┐
                              │     COMPLETE NOSQL MASTERY          │
                              │ Query Fluency + Storage Internals   │
                              └─────────────────────────────────────┘
```

---

## 3. Representative Primary Databases

| Category | Primary System | Concrete Specification | Local Port |
| :--- | :--- | :--- | :--- |
| **Document** | **MongoDB** | MongoDB Query Language & Aggregation Pipeline v7.0+ | `27017` |
| **Wide-Column** | **Apache Cassandra** | CQL v3.4.7 & Cassandra 5.0 Storage Attached Indexing | `9042` |
| **Cloud KV / Document** | **Amazon DynamoDB** | Native Query/Update Expressions & PartiQL v1.0 | `8000` |
| **In-Memory Structures**| **Redis** | Redis Commands & RedisSearch / RedisJSON v7.4 | `6379` |
| **Property Graph** | **Neo4j** | Cypher 5 & ISO/IEC 39075:2024 (GQL) Alignment | `7474`, `7687` |
| **Search Engine** | **Elasticsearch** | Elasticsearch JSON Query DSL & Aggregations v8.17 | `9200` |

---

## 4. The 10-Step Core Learning Cycle

Every phase adheres strictly to the 10-step pedagogical cycle:

```text
REQUIREMENT ──► ACCESS PATTERN ──► MODEL DATA ──► PREDICT ──► WRITE QUERY
     ▲                                                             │
     │                                                             ▼
  EXPLAIN ◄── REMODEL / REINDEX ◄── BREAK & DEBUG ◄── MEASURE ◄── INSPECT
```

1. **Requirement:** State the exact business or analytical objective.
2. **Access Pattern:** Catalog trigger, frequency, input keys, and SLA.
3. **Model Data:** Design the physical document, table, or graph schema.
4. **Predict:** Formulate explicit hypotheses about partitions and scanned records.
5. **Write Query:** Formulate the native query or pipeline.
6. **Inspect:** Run `explain()`, execution stats, or query tracing.
7. **Measure:** Calculate read amplification (`Records Examined / Records Returned`).
8. **Break & Debug:** Intentionally trigger full scans or hot partitions and diagnose.
9. **Remodel:** Restructure keys or compound indexes to restore $O(1)$ or $O(\log N)$ performance.
10. **Explain:** Articulate the physical storage journey in plain engineering terms.

---

## 5. Repository Structure

```text
nosql-databases-and-query-languages-from-scratch/
├── README.md                      # Repository Manifesto, progression, quickstart
├── ROADMAP.md                     # Exhaustive 264-phase roadmap across 23 parts
├── LEARNING.md                    # The 10-step learning cycle & 15 non-negotiable rules
├── LESSON_TEMPLATE.md             # Canonical 22-section lesson format
├── QUERY_TEMPLATE.md              # Canonical 20-section query exercise format
├── VERSIONS.md                    # Pinned versions, ports, and specification matrix
├── COST_SAFETY.md                 # 100% Local-first zero-cost execution guide
├── CONTRIBUTING.md                # Pedagogical contribution standards
├── LICENSE                        # MIT License
├── Makefile                       # Developer automation targets
├── docker-compose.yml             # Multi-profile container orchestrator
├── outputs/
│   └── evidence-template.md       # Standardized evidence workbook
├── docs/                          # Authoritative architectural guides
│   ├── glossary.md                # 20+ first-principles storage definitions
│   ├── mental-models.md           # Physical storage realities & engine comparisons
│   ├── query-thinking.md          # The 18-question query evaluation framework
│   ├── access-patterns.md         # Cross-industry access pattern catalog
│   ├── database-selection.md      # Multi-dimensional decision trees & matrices
│   ├── consistency.md             # CAP, PACELC, Quorum math (N, R, W), CRDTs
│   ├── troubleshooting.md         # Operational diagnostic playbooks
│   └── anti-patterns.md           # The 17 fatal NoSQL anti-patterns analyzed
├── phases/                        # 264 curriculum phases (Phase 00 to 263)
├── exercises/                     # 260 query exercises across 4 tiers
│   ├── beginner/                  # 70 foundational exercises
│   ├── intermediate/              # 80 compound & aggregation exercises
│   ├── advanced/                  # 60 partition-aware & graph exercises
│   └── challenge/                 # 50 cross-paradigm & schema redesign exercises
├── drills/                        # 140 muscle-memory query drills across 7 categories
├── broken-databases/              # 45 forensic failure & debugging labs
├── datasets/                      # Rich cross-paradigm seed datasets (JSON)
├── simulations/                   # 6 standalone Python storage & consensus simulators
├── benchmarks/                    # Automated query latency & throughput harnesses
├── projects/                      # 10 substantial engineering projects
├── capstones/                     # 9 comprehensive architectural capstones
└── solutions/                     # Separated reference solutions
```

---

## 6. Quickstart: Getting Started in 2 Minutes

### Step 1: Verify Host Environment
```bash
./scripts/check-environment.sh
```

### Step 2: Generate Pristine Datasets
```bash
python3 scripts/seed-data.py
```

### Step 3: Run Distributed Systems Simulators (Zero External Dependencies)
```bash
make test-simulations
```

### Step 4: Launch Database Containers (Choose Profile)
```bash
# Start MongoDB only:
./scripts/start-lab.sh mongo

# Or start all 6 engines:
./scripts/start-lab.sh all
```

### Step 5: Begin Phase 00
Navigate to [Phase 00: NoSQL Laboratory](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/phases/phase-00-nosql-laboratory/docs/en.md) and open the evidence workbook at [`outputs/evidence-template.md`](file:///Users/tushar/desktop/private/repos/nosql-databases-and-query-languages-from-scratch/outputs/evidence-template.md).
