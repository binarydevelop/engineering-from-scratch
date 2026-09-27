# elasticsearch-from-scratch

> **Motto:** Understand it. Build it. Index it. Search it. Measure it. Break it. Recover it. Scale it. Ship it.

A first-principles, hands-on engineering course to deeply understand Elasticsearch as a distributed search and analytics engine built around Apache Lucene, immutable segments, sharding, replication, and query coordination.

---

## 1. Why This Repository Exists

Most software engineers treat Elasticsearch as **"a database with a search box."**

That mental model is dangerous. It leads directly to production disasters:
* Mapping explosions that crash the elected master node.
* Oversharding that consumes gigabytes of JVM heap on empty indices.
* Running full-text wildcard queries (`*search*`) that peg coordinator CPUs at 100%.
* Aggregating on analyzed `text` fields that trigger OutOfMemory circuit breaker trips.
* Treating replica shards as backups and losing all data during human error.

This course systematically replaces that shallow API memorization with deep systems intuition:

$$\textbf{Elasticsearch is a distributed document-oriented search and analytics engine built around Lucene indexes, immutable segments, sharding, replication, and query coordination.}$$

---

## 2. The Curriculum Progression

```text
Document Scan (O(N) Table Scan)
       │
       ▼
Inverted Index (O(1) Postings Lists)
       │
       ▼
Tokenization & Normalization (Text to Searchable Terms)
       │
       ▼
Analysis Pipeline (Char Filters -> Tokenizer -> Token Filters)
       │
       ▼
Relevance Ranking (TF-IDF -> BM25 Saturation & Length Norm)
       │
       ▼
Mappings & Schema (Text vs Keyword & Doc Values)
       │
       ▼
Segments & Storage (Immutable Lucene Files on Disk)
       │
       ▼
Near-Real-Time Search (Refresh vs Flush vs Translog)
       │
       ▼
Distributed Aggregations (Columnar Doc Values Map-Reduce)
       │
       ▼
Shards & Routing (Partitioning the Index)
       │
       ▼
Replicas & High Availability (Failover & Read Scaling)
       │
       ▼
Distributed Search (Two-Phase Query-Then-Fetch)
       │
       ▼
Cluster Operations (Observability, Watermarks, Capacity Planning)
       │
       ▼
Capstones (E-Commerce Catalog, Log Analytics, Mini Search Engine)
```

---

## 3. Strict Version Discipline

All examples, REST commands, docker compose topologies, and Python clients are pinned to official stable releases:

| Component | Pinned Version | Notes |
| :--- | :--- | :--- |
| **Elasticsearch** | **8.17.0** | Official Docker image `docker.elastic.co/elasticsearch/elasticsearch:8.17.0` |
| **Apache Lucene** | **9.12.0** | Underlying index and segment engine bundled in ES 8.17.0 |
| **Python Client** | **8.17.0+** | Modern typed connection pool (`elasticsearch>=8.17.0,<9.0.0`) |
| **Python Runtime**| **3.11+ / 3.12+ / 3.14** | Native standard library + requests + pytest |

See [VERSIONS.md](VERSIONS.md) for detailed release notes and behavioral differences between Elasticsearch versions.

---

## 4. The Pedagogical Methodology

Every lesson in this repository follows the strict experimental loop outlined in [LEARNING.md](LEARNING.md):

```text
MOTTO ──► PROBLEM ──► PREDICT ──► FIRST PRINCIPLES ──► BUILD IT ──► USE ELASTICSEARCH
   ▲                                                                         │
   │                                                                         ▼
EVIDENCE ◄── WHAT NEXT ◄── MODIFY IT ◄── RECOVER IT ◄── BREAK IT ◄── MEASURE IT
```

### The Rule of Completion
A lesson is **NOT** complete because a curl query returned HTTP 200. You are finished only when you can:
1. Explain the underlying physical data structure.
2. Predict query behavior before running it.
3. Build the simplified mechanism from scratch in pure Python.
4. Intentionally misconfigure or break the system.
5. Diagnose the failure from error logs and allocation explainers.
6. Recover the system to a healthy green state.
7. Record observed measurements in your evidence log.

---

## 5. Repository Structure

```text
elasticsearch-from-scratch/
├── README.md                          # Repository overview and philosophy
├── ROADMAP.md                         # Detailed curriculum map for all 88 phases
├── LEARNING.md                        # The learning methodology and mastery loop
├── LESSON_TEMPLATE.md                 # Universal template for all lessons
├── VERSIONS.md                        # Pinned version specifications (ES 8.17, Lucene 9.12)
├── CONTRIBUTING.md                    # Contribution guidelines
├── Makefile                           # Automation shortcuts (Make != Docker != ES)
├── docker-compose.yml                 # Single-node lab environment
├── docker-compose.cluster.yml         # 3-node distributed cluster lab
├── requirements.txt                   # Python dependencies
│
├── docs/                              # Deep technical reference guides
│   ├── glossary.md                    # 40+ formal Information Retrieval & ES definitions
│   ├── mental-models.md               # ASCII architectural diagrams & pipelines
│   ├── query-reference.md             # Canonical Query DSL & Aggregations cheatsheet
│   └── troubleshooting.md             # Field guide for diagnosing Red/Yellow clusters
│
├── scripts/                           # Operational scripts
│   ├── check-environment.sh          # Pre-flight environment verifier
│   ├── start-elasticsearch.sh        # Docker Compose launcher with readiness probes
│   ├── stop-elasticsearch.sh         # Graceful shutdown script
│   ├── reset-lab.sh                  # Wipes user indices and resets cluster blocks
│   └── run-all-tests.py              # Automated test suite across all 90 targets
│
├── phases/                            # 88 Dependency-ordered phases (00 through 87)
│   ├── 00-environment-and-search-lab/
│   ├── 01-why-search-engines-exist/
│   ├── ...
│   └── 87-final-mental-model/
│
└── projects/                          # Capstone systems
    ├── product_search/                # Capstone 1: Faceted E-Commerce Catalog Search
    ├── log_search/                    # Capstone 2: Structured APM & Microservice Logging
    ├── mini_search_engine/            # Capstone 3: Pure Python Search Engine from scratch
    └── distributed_simulator/         # Distributed Scatter-Gather Cluster Simulator
```

---

## 6. Getting Started

### Step 1: Pre-flight Verification
Verify that your machine has Python 3.11+, Docker, Docker Compose, and curl:
```bash
./scripts/check-environment.sh
```

### Step 2: Launch the Elasticsearch Lab
Start the single-node Elasticsearch 8.17.0 lab container in the background:
```bash
make up
```
*Wait ~10 seconds until the script confirms:*
```text
Elasticsearch is ONLINE! Cluster status: green
```

### Step 3: Run the Automated Validation Suite
Execute tests across all 88 phases and capstone implementations:
```bash
make test
```
*(All 90 test cases should pass cleanly).*

### Step 4: Begin Lesson 01
Navigate to Phase 01:
```bash
cd phases/01-why-search-engines-exist
cat docs/en.md
```
Follow the prediction step, run the experiment, and start building your search engine intuition!

---

## 7. The Three Capstone Projects

* **Capstone 1: E-Commerce Product Search ([projects/product_search/](projects/product_search/))**
  A complete product search service with full-text BM25 multi-matching (`title^3`, `brand^2`), typo resilience (`fuzziness: AUTO`), edge n-gram autocomplete suggestions, and dynamic multi-tier bucket aggregations.
* **Capstone 2: Microservice Log Search & APM Analytics ([projects/log_search/](projects/log_search/))**
  Time-series telemetry engine ingesting structured logs, computing date-histogram error spikes, and calculating p95 service response times via T-Digest.
* **Capstone 3: Mini Search Engine From Scratch ([projects/mini_search_engine/](projects/mini_search_engine/))**
  A standalone, dependency-free information retrieval engine written in pure Python 3 standard library: positional inverted index, columnar doc values, probabilistic BM25 ranking, and boolean query execution.

---

## 8. What You Will Be Able to Answer

Upon finishing this curriculum, you will answer questions like an infrastructure architect:

* Why does full-text search require an inverted index rather than a B-Tree?
* What is the physical lifecycle of a document from `POST /_doc` to disk?
* Why is Elasticsearch near-real-time (NRT) rather than immediately searchable?
* How does BM25 solve the two fatal flaws of classic TF-IDF?
* Why does deleting a document initially *increase* disk usage?
* What is the difference between a Refresh (memory to OS cache) and a Flush (`fsync` to disk)?
* Why is setting JVM heap larger than 31 GB counter-productive?
* How does Query-Then-Fetch prevent network saturation across hundreds of shards?
* What causes hot shards and how do you diagnose them using `hot_threads`?
* Why does setting `number_of_replicas: 1` turn a single-node cluster YELLOW?
* How do you execute zero-downtime reindexing using index aliases?
* In what scenarios is Elasticsearch the **wrong** tool compared to PostgreSQL, Redis, or Kafka?

---

## Final Mental Model

> **Elasticsearch is no longer a black box.**
>
> We started by scanning documents, built an inverted index, added tokenization and ranking, learned how immutable segments make search possible, distributed those indexes across shards, replicated them for resilience, and used the resulting system for real search and analytics workloads.
>
> Now when Elasticsearch appears inside a system architecture, we can reason about why it is there, how indexing and search work, what it costs, how it fails, and whether a simpler data system would be more appropriate.
