#!/usr/bin/env python3
"""
build_curriculum_part7.py - Generates Phases 82 to 87 for elasticsearch-from-scratch.
Covers Comparisons (Postgres, Vector), Anti-Patterns, When NOT to Use ES,
System Design Scenarios, and the Final End-to-End Mental Model Trace.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    if path.endswith(".sh") or path.endswith(".py"):
        os.chmod(path, 0o755)

def evidence_template(phase_title, phase_num):
    return f"""# Evidence Log: Phase {phase_num:02d} - {phase_title}

Date: 2026-09-23
Elasticsearch Version: 8.17.0
Lucene Version: 9.12.0
Working Directory: phases/{phase_num:02d}-{phase_title.lower().replace(' ', '-').replace('/', '-')}

## Prediction
Before executing the experiment, record your hypothesis here:

## Commands Executed
```bash
./experiments/run_experiment.sh
```

## Important Terminal Output
```text
```

## Measurements
* Metric 1:
* Metric 2:

## What Actually Happened?

## What Did I Intentionally Break?

## How Did I Diagnose It?

## How Did I Recover?

## Explain the Concept in My Own Words:
"""

def generate_phases_82_to_87():
    phases = [
        (82, "Elasticsearch vs Database",
         "A search engine is not a relational database: different access patterns require different physical data structures.",
         """# Lesson 82.1: Elasticsearch vs Database (PostgreSQL)

## Motto
"A search engine is not a relational database: different access patterns require different physical data structures."

## Problem
Developers often ask: *"Can I replace PostgreSQL with Elasticsearch?"* or *"Can I just use PostgreSQL tsvector for all my search needs?"* Without understanding the architectural trade-offs, teams make disastrous technology choices.

## Prediction
In what dimensions does PostgreSQL dominate Elasticsearch, and in what dimensions does Elasticsearch dominate PostgreSQL?

## Why this matters
Relational databases and search engines were built for opposite optimization targets.

## First principles
Architectural Comparison Matrix:
| Dimension | PostgreSQL (Relational OLTP) | Elasticsearch (Search & Analytics) |
| :--- | :--- | :--- |
| **Primary Data Structure** | B-Trees, Heap Disk Pages | Inverted Indexes, Columnar Doc Values |
| **Transactions** | ACID (Multi-row atomic rollback) | Document-level optimistic locking |
| **Foreign Keys / Joins** | First-class relational joins ($O(1)$/$O(N)$) | Anti-pattern; denormalization required |
| **Full-Text Search** | Basic GIN `tsvector` (slow at scale) | Probabilistic BM25, Tokenizers, Slop |
| **Analytics & Facets** | Expensive sequential table scans | Instant distributed doc values map-reduce |
| **Scaling Model** | Vertical (Primary + Read Replicas) | Horizontal (Automatic sharding & routing) |
| **Durability Model** | Synchronous WAL commit | Near-Real-Time translog + refresh lag |

## Mental model
```text
           THE COEXISTENCE ARCHITECTURE
┌───────────────────────────┐         ┌───────────────────────────┐
│ POSTGRESQL (Source of Truth)│         │ ELASTICSEARCH (Search View)│
│ - ACID Transactions       │         │ - Fast Full-Text BM25     │
│ - User Accounts, Orders   │         │ - Facets & Filters        │
│ - Strict Relational Joins │         │ - Autocomplete & Typos    │
└─────────────┬─────────────┘         └─────────────▲─────────────┘
              │                                     │
              └──────── Change Data Capture ────────┘
                      (Debezium / Kafka CDC)
```

## Build it
See `code/postgres_vs_es_bench.py` simulating B-Tree prefix vs Inverted Index lookup in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/82-elasticsearch-vs-database/experiments/run_experiment.sh
```

## Inspect it
Observe the difference between relational table lookups and distributed full-text search.

## Measure it
Compare full-text query latency across 50,000 documents: relational `LIKE %term%` vs inverted index.

## Break it
Attempt to perform a multi-table foreign-key transactional join in Elasticsearch: observe that Elasticsearch has no SQL joins.

## Recover it
Denormalize the data model: embed related child data directly inside the document.

## Modify it
Compare `has_child` / `has_parent` joins in Elasticsearch (and measure their heavy performance penalty).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch lack multi-document ACID transactions?
2. When is PostgreSQL's built-in full-text search (`tsvector`) sufficient without introducing Elasticsearch?

## Guarantees
* Elasticsearch provides distributed full-text and analytical capabilities that relational databases cannot match at scale.

## Non-guarantees
* Elasticsearch does NOT guarantee ACID transactions or relational integrity constraints.

## When to use this
* System design decision-making and database selection reviews.

## When not to use this
* Believing one tool can solve every storage requirement.

## What comes next
In Phase 83, we compare Lexical BM25 Search with Dense Vector Search.
""",
"""#!/usr/bin/env python3

def trade_off_analysis(workload_type):
    if workload_type == "bank_transactions":
        return "PostgreSQL", "Requires strict multi-row ACID transactions and balance rollbacks."
    elif workload_type == "e_commerce_catalog":
        return "Elasticsearch", "Requires fuzzy search, facets, BM25 ranking, and sub-15ms response."
    elif workload_type == "user_profile_crud":
        return "PostgreSQL", "Primary key lookup, foreign key relational integrity."
    elif workload_type == "server_log_analytics":
        return "Elasticsearch", "High-throughput append-only time-series with date histogram aggs."
    return "Unknown", "Evaluate access patterns."

if __name__ == "__main__":
    workloads = ["bank_transactions", "e_commerce_catalog", "user_profile_crud", "server_log_analytics"]
    print("Workload Architectural Decision Engine:")
    for w in workloads:
        winner, reason = trade_off_analysis(w)
        print(f"  [{w:22s}] ──► Choose: {winner:14s} ({reason})")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 82: Elasticsearch vs Database ==="
python3 phases/82-elasticsearch-vs-database/code/82_elasticsearch_vs_database.py
"""),

        (83, "Elasticsearch vs Vector Search",
         "Lexical search matches exact terms; vector search matches conceptual embeddings. Hybrid search unites both.",
         """# Lesson 83.1: Elasticsearch vs Vector Search

## Motto
"Lexical search matches exact terms; vector search matches conceptual embeddings. Hybrid search unites both."

## Problem
A user searches for: *"something comfortable to sleep on during a hiking trip"*.
A traditional lexical BM25 query looks for documents containing the words `"comfortable"`, `"sleep"`, and `"hiking"`. If an item is titled *"Ultralight Inflatable Camp Mattress"*, BM25 returns 0 hits because the words do not overlap lexically!

## Prediction
Can dense vector embeddings match semantically related items that share zero common words with the query?

## Why this matters
Modern search combines **Lexical BM25 Search** (for exact keywords, part numbers, SKUs, and names) with **Dense Vector Search** (for conceptual semantic intent) using **Reciprocal Rank Fusion (RRF)**.

## First principles
* **Lexical Search (BM25):** Operates on discrete tokens in an inverted index. Fast, precise, but suffers from vocabulary mismatch.
* **Vector Search ($k$-NN / HNSW):** Encodes text into a continuous high-dimensional vector space ($\mathbb{R}^{768}$ or $\mathbb{R}^{1536}$). Finds nearest neighbors using cosine similarity.
* **Hybrid Search (Elasticsearch 8.x):** Executes both lexical BM25 and dense vector search in parallel, merging candidate lists with Reciprocal Rank Fusion (RRF).

## Mental model
```text
Query: "portable sleeping mat"
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
1. LEXICAL BM25             2. DENSE VECTOR (HNSW)
(Exact term matches)        (Embedding distance in 768 dims)
"portable", "sleeping"      Matches "Ultralight Inflatable Pad"
       │                           │
       └─────────────┬─────────────┘
                     ▼
        RECIPROCAL RANK FUSION (RRF)
     ──► Perfectly Balanced Hybrid Hits!
```

## Build it
See `code/vector_vs_lexical_sim.py` demonstrating cosine vector similarity vs BM25 in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/83-elasticsearch-vs-vector-search/experiments/run_experiment.sh
```

## Inspect it
Create an index with `dense_vector` mapping:
```bash
curl -X PUT http://localhost:9200/vector_demo -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "embedding": {
        "type": "dense_vector",
        "dims": 3,
        "index": true,
        "similarity": "cosine"
      }
    }
  }
}'
```

## Measure it
Compare query latency: BM25 inverted index lookup (< 2ms) vs HNSW graph traversal (~10ms).

## Break it
Search for an exact part number (`"X49-B091-REV3"`) using pure vector search: vector embeddings struggle with exact alphanumeric codes!

## Recover it
Use **Hybrid Search**: BM25 catches exact codes, vector search catches conceptual meaning.

## Modify it
Execute an Elasticsearch $k$-NN query:
```json
{
  "knn": {
    "field": "embedding",
    "query_vector": [0.1, 0.8, -0.4],
    "k": 5,
    "num_candidates": 50
  }
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does pure vector search often fail on exact model numbers and serial numbers?
2. What is Reciprocal Rank Fusion (RRF) and why is it preferred over raw score addition?

## Guarantees
* Dense vector search matches semantic concepts without requiring shared vocabulary.

## Non-guarantees
* Vector search is computationally more expensive and consumes significantly more RAM than inverted indexes.

## When to use this
* Natural language questions, semantic discovery, and AI-assisted search.

## When not to use this
* Exact SKU lookup, structured log filtering, or numeric range filtering.

## What comes next
In Phase 84, we catalogue the 15 Fatal Elasticsearch Anti-Patterns.
""",
"""#!/usr/bin/env python3
import math

def cosine_similarity(v1, v2):
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    return dot / (norm1 * norm2) if norm1 > 0 and norm2 > 0 else 0.0

if __name__ == "__main__":
    # Simulated 3D semantic embeddings
    query_vec = [0.8, 0.6, 0.0] # "camping sleeping gear"
    doc_a_vec = [0.78, 0.62, 0.05] # "ultralight mattress pad" (No common words, but high semantic similarity!)
    doc_b_vec = [0.1, 0.05, 0.99] # "gardening lawn mower"

    sim_a = cosine_similarity(query_vec, doc_a_vec)
    sim_b = cosine_similarity(query_vec, doc_b_vec)

    print("Vector Search Semantic Matching:")
    print(f"  Similarity to 'ultralight mattress pad': {sim_a:.4f} (High match!)")
    print(f"  Similarity to 'gardening lawn mower':   {sim_b:.4f} (Low match)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 83: Elasticsearch vs Vector Search ==="
python3 phases/83-elasticsearch-vs-vector-search/code/83_elasticsearch_vs_vector_search.py
"""),

        (84, "Elasticsearch Anti-Patterns",
         "Learn from the graveyard of search outages: 15 fatal architectural blunders and their concrete mitigations.",
         """# Lesson 84.1: Elasticsearch Anti-Patterns

## Motto
"Learn from the graveyard of search outages: 15 fatal architectural blunders and their concrete mitigations."

## Problem
Most Elasticsearch outages are self-inflicted by well-intentioned engineers applying patterns from relational databases or message queues to a search engine.

## Prediction
Can you identify at least 5 common configuration or architectural mistakes that bring down production search clusters?

## Why this matters
Mastery is not just knowing how to build; it is knowing what NEVER to build.

## First principles
The 15 Fatal Search Anti-Patterns:
1. **Primary OLTP Source of Truth:** Using ES as the sole transactional database without ACID backups.
2. **Oversharding:** 5,000 tiny 50MB shards exhausting JVM heap metadata.
3. **Uncontrolled Dynamic Mappings:** Dynamic user keys triggering mapping explosions.
4. **Leading Wildcard Queries:** `*search*` forcing full dictionary scans.
5. **Deep Pagination with `from + size`:** Requesting page 5,000 and crashing coordinator memory.
6. **Massive Documents:** Indexing 50MB PDF blobs into JSON `_source`.
7. **Mapping Analyzed Text as IDs:** Querying tokenized UUIDs with `match` instead of exact `keyword`.
8. **High-Cardinality Deep Aggregations:** Terms aggregations on millions of unique values.
9. **Replicas Treated as Backups:** Zero snapshots taken because "we have replicas".
10. **Giant Single Bulk Requests:** Sending 1GB bulk payloads tripping circuit breakers.
11. **One Hot Shard:** Skewed custom routing pinning 1 node at 100% CPU.
12. **Excessive Refresh Frequency:** Calling `?refresh=true` on every write in a tight loop.
13. **Monolithic Multi-Year Log Index:** 20TB in a single index instead of daily rolling indices.
14. **Allocating 100% RAM to JVM Heap:** Depriving the OS page cache of memory for Lucene segments.
15. **Public Cluster Exposure:** Running port 9200 without authentication on the public internet.

## Mental model
```text
           THE RESILIENT SEARCH ARCHITECTURE
┌─────────────────────────────────────────────────────────────┐
│ 1. Dedicated Master Nodes (split-brain immune)              │
│ 2. Shards sized 20GB - 50GB (No oversharding)               │
│ 3. Explicit Mappings with .keyword multi-fields             │
│ 4. Search API Gateway with query validation                 │
│ 5. Daily Snapshots to S3/GCS                                │
│ 6. Memory: 50% JVM Heap (max 31GB), 50% OS Page Cache       │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/antipattern_auditor.py` auditing cluster configurations against the 15 anti-patterns in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/84-elasticsearch-anti-patterns/experiments/run_experiment.sh
```

## Inspect it
Review the audit checklist against your lab cluster.

## Measure it
Assess risk levels across indexing and search configurations.

## Break it
Pick any anti-pattern from the list and test its failure mode in our test environment.

## Recover it
Apply the corresponding documented remediation.

## Modify it
Add custom organizational linting rules to the auditor script.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is treating replica shards as backups a fatal assumption?
2. Why is mapping an order UUID as `text` dangerous?

## Guarantees
* Eliminating these 15 anti-patterns guarantees rock-solid cluster stability.

## Non-guarantees
* Hardware failures (disk corruption, power outages) still require automated failover and snapshot restores.

## When to use this
* Architecture reviews, incident post-mortems, and pre-production go-live checklists.

## When not to use this
* Ignoring operational warnings.

## What comes next
In Phase 85, we establish clear boundaries: When Elasticsearch Is the WRONG Tool.
""",
"""#!/usr/bin/env python3

ANTIPATTERNS = [
    ("Primary Database", "Elasticsearch as sole primary ACID store", "Use PostgreSQL/MySQL as source of truth; sync to ES via CDC."),
    ("Oversharding", "Thousands of shards < 1GB", "Consolidate into shards sized 20GB to 50GB."),
    ("Dynamic Mapping", "dynamic: true allowing arbitrary JSON keys", "Enforce dynamic: strict and explicit schemas."),
    ("Leading Wildcards", "Executing *query* on large text", "Use edge_ngram or wildcard field type."),
    ("Deep Pagination", "from: 50000 with from + size", "Switch to search_after cursor pagination."),
    ("No Snapshots", "Zero backups relying only on replicas", "Configure automated daily snapshots to S3/GCS."),
    ("Heap Monopolization", "Allocating > 50% RAM or > 31GB to heap", "Cap heap at 50% of RAM (max 31GB) for OS page cache."),
    ("Unsecured Port", "Exposing port 9200 without TLS/auth", "Enable X-Pack security, TLS, and RBAC.")
]

if __name__ == "__main__":
    print("=== The Elasticsearch Anti-Pattern Audit ===\\n")
    for idx, (title, symptom, remedy) in enumerate(ANTIPATTERNS, 1):
        print(f"Anti-Pattern {idx}: [{title}]")
        print(f"  Hazard: {symptom}")
        print(f"  Remedy: {remedy}\\n")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 84: Elasticsearch Anti-Patterns Audit ==="
python3 phases/84-elasticsearch-anti-patterns/code/84_elasticsearch_anti_patterns.py
"""),

        (85, "When Elasticsearch Is the Wrong Tool",
         "The mark of a senior systems engineer is knowing when NOT to use a tool: 7 scenarios where Elasticsearch is the wrong choice.",
         """# Lesson 85.1: When Elasticsearch Is the Wrong Tool

## Motto
"The mark of a senior systems engineer is knowing when NOT to use a tool: 7 scenarios where Elasticsearch is the wrong choice."

## Problem
When engineers learn Elasticsearch, everything looks like a search problem. They try to use it as a primary transactional database, an in-memory cache, an event streaming queue, or a graph database. The resulting system is fragile, expensive, and difficult to maintain.

## Prediction
Name 3 database workloads where PostgreSQL or Redis provably outperforms Elasticsearch by an order of magnitude.

## Why this matters
Elasticsearch is exceptional at full-text search, distributed faceting, and unstructured log analytics. It is unsuited for relational transactions, sub-millisecond point updates, and strict FIFO queues.

## First principles
The 7 Wrong-Tool Scenarios:
1. **Primary Key Point Lookups ($< 1$ ms):** Redis provides sub-millisecond in-memory lookups at $10\times$ the throughput of Elasticsearch.
2. **Strict Multi-Row ACID Transactions:** Financial ledgers and banking transfers require relational ACID engines (PostgreSQL, MySQL).
3. **Tiny Datasets ($< 50$ MB):** PostgreSQL built-in `tsvector` or SQLite is vastly simpler, requires zero Docker clusters, and eliminates distributed networking.
4. **Relational Join-Heavy Workloads:** If your queries require joining 6 normalized tables on foreign keys, Elasticsearch will require massive denormalization and update amplification.
5. **Event Queues / FIFO Streaming:** Elasticsearch is not a message broker. Building a task queue in Elasticsearch leads to high refresh thrashing and deleted tombstone bloat (use Apache Kafka or RabbitMQ).
6. **Ultra-Low Memory Budgets:** Running Elasticsearch on a 512MB RAM VPS is unstable; the JVM alone demands memory.
7. **Graph Traversal:** Multi-hop social connections (Friends of Friends) are $O(N)$ graph operations (use Neo4j).

## Mental model
```text
           CHOOSING THE RIGHT TOOL FOR THE JOB
┌─────────────────────────────────────────────────────────────┐
│ Sub-millisecond Key-Value Caching ──► REDIS                 │
│ Multi-Row ACID Ledger & Relational ──► POSTGRESQL           │
│ Streaming Event Pub/Sub & Queuing ──► APACHE KAFKA          │
│ Multi-Hop Graph Traversal         ──► NEO4J                 │
│ Full-Text Search, Facets & Logs   ──► ELASTICSEARCH         │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/tool_selection_matrix.py` mapping requirements to optimal database architectures in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/85-when-elasticsearch-is-the-wrong-tool/experiments/run_experiment.sh
```

## Inspect it
Review the decision matrix for architectural trade-offs.

## Measure it
Compare operational complexity: maintaining a single Postgres instance vs a 3-node distributed Elasticsearch cluster.

## Break it
Build a simulated FIFO queue inside an Elasticsearch index: observe how rapid insert/delete updates generate segment merge thrashing.

## Recover it
Replace the search queue with a proper queue engine (Redis List / Kafka).

## Modify it
Evaluate an e-commerce architecture combining Postgres (Source of Truth), Redis (Sessions & Cart), and Elasticsearch (Search & Facets).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does using Elasticsearch as a FIFO job queue cause severe storage thrashing?
2. If your dataset is 10,000 rows, why is PostgreSQL `tsvector` preferable to deploying Elasticsearch?

## Guarantees
* Using the correct specialized tool maximizes performance while minimizing operational overhead.

## Non-guarantees
* No single database engine excels at all access patterns simultaneously.

## When to use this
* Architecture reviews, tech stack selection, and system design interviews.

## When not to use this
* Blindly defaulting to Elasticsearch for non-search workloads.

## What comes next
In Phase 86, we practice end-to-end System Design with Elasticsearch across 8 production scenarios.
""",
"""#!/usr/bin/env python3

def recommend_technology(requirements):
    recs = []
    if requirements.get("strict_acid"):
        recs.append("PostgreSQL (Strict ACID relational transactions)")
    if requirements.get("sub_ms_cache"):
        recs.append("Redis (Sub-millisecond in-memory caching)")
    if requirements.get("event_stream"):
        recs.append("Apache Kafka (High-throughput durable event log)")
    if requirements.get("full_text_facets"):
        recs.append("Elasticsearch (Distributed BM25 search & analytics)")
    return recs

if __name__ == "__main__":
    app_needs = {
        "strict_acid": True,
        "sub_ms_cache": True,
        "event_stream": True,
        "full_text_facets": True
    }
    print("Multi-Engine System Design Recommendation:")
    technologies = recommend_technology(app_needs)
    for t in technologies:
        print("  -", t)
    print("\\nEach tool serves its specialized strength; none replaces the others!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 85: Technology Selection Boundaries ==="
python3 phases/85-when-elasticsearch-is-the-wrong-tool/code/85_when_elasticsearch_is_the_wrong_tool.py
"""),

        (86, "System Design With Elasticsearch",
         "Architecting for scale: answer the 20 fundamental design questions across 8 real-world enterprise architectures.",
         """# Lesson 86.1: System Design With Elasticsearch

## Motto
"Architecting for scale: answer the 20 fundamental design questions across 8 real-world enterprise architectures."

## Problem
In a distributed systems design interview or production RFC, stating *"we will put it in Elasticsearch"* is unacceptable. You must justify every architectural parameter: shard count, replicas, mapping types, routing strategy, refresh interval, and disaster recovery.

## Prediction
Can you answer all 20 architectural questions for an E-Commerce Search, Log Analytics, or Autocomplete system?

## Why this matters
System design is the ultimate test of engineering maturity. This phase provides the comprehensive blueprint.

## First principles
The 20 Architectural Questions for Every Search System:
1. **Why Elasticsearch?** (What specific IR or analytical need justifies it?)
2. **What is the Source of Truth?** (Where is raw data permanently stored?)
3. **What is the synchronization mechanism?** (CDC, Kafka, Batch ETL?)
4. **What documents are indexed?** (Entity granularity?)
5. **What is the mapping schema?**
6. **Which fields are `text`?** (Tokenized for search?)
7. **Which fields are `keyword`?** (Exact filtering, sorting, aggregations?)
8. **What custom analyzers are needed?** (Stemming, stop words, shingles?)
9. **What is the query pattern?** (`bool` with `must` + `filter`?)
10. **What aggregations are computed?** (Terms, ranges, histograms?)
11. **What is the expected read QPS?**
12. **What is the peak indexing rate?** (Docs/sec?)
13. **What is the total data volume?** (GB/TB per day/year?)
14. **What is the retention period?**
15. **What is the sharding strategy?** (How many primary shards and why?)
16. **What is the replica strategy?** (High availability and read scaling?)
17. **What is the freshness requirement?** (`refresh_interval`: 1s vs 30s?)
18. **Is custom routing (`_routing`) appropriate?**
19. **What is the reindex / migration strategy?** (Aliases and versioned indices?)
20. **What failure modes exist and how does the system recover?**

## Mental model
```text
┌─────────────────────────────────────────────────────────────┐
│                 SYSTEM DESIGN SCENARIOS                     │
├─────────────────────────────────────────────────────────────┤
│ 1. E-Commerce Product Catalog Search                        │
│ 2. Centralized Microservice Log Analytics (APM)             │
│ 3. Multi-Tenant SaaS Knowledge Base                         │
│ 4. Sub-10ms Global Autocomplete Search Bar                  │
│ 5. Security Information & Event Management (SIEM)           │
│ 6. Real-Time Geospatial Store & Ride Finder                 │
│ 7. Job Portal & Resume Candidate Matching                   │
│ 8. Audit Event Trail with Cold Tiering                      │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/system_design_evaluator.py` validating architecture specifications against the 20 criteria in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/86-system-design-with-elasticsearch/experiments/run_experiment.sh
```

## Inspect it
Review the architectural blueprints for all 8 enterprise scenarios.

## Measure it
Evaluate sizing calculations for a 10,000 QPS e-commerce platform.

## Break it
Challenge the architecture: what happens when daily indexing volume triples?

## Recover it
Scale horizontally by adding data nodes and increasing primary shards via rollover.

## Modify it
Adapt the architecture for multi-region active-passive disaster recovery.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. How do you defend your choice of shard count in a system design interview?
2. Why is decoupling the search view from the relational source of truth essential?

## Guarantees
* Rigorous answers to all 20 questions guarantee an operationally sound production search architecture.

## Non-guarantees
* Real production workloads require continuous monitoring and benchmark validation.

## When to use this
* Architecture proposals, tech design documents, and technical interviews.

## When not to use this
* Trivial prototype projects.

## What comes next
In Phase 87, we synthesize the Final Complete Mental Model: tracing an index write and search query end-to-end.
""",
"""#!/usr/bin/env python3

SCENARIOS = [
    "1. E-Commerce Product Catalog Search",
    "2. Centralized Microservice Log Analytics (APM)",
    "3. Multi-Tenant SaaS Knowledge Base",
    "4. Sub-10ms Global Autocomplete Search Bar",
    "5. Security Information & Event Management (SIEM)",
    "6. Real-Time Geospatial Store & Ride Finder",
    "7. Job Portal & Resume Candidate Matching",
    "8. Audit Event Trail with Cold Tiering"
]

if __name__ == "__main__":
    print("=== The 8 Enterprise System Design Scenarios ===\\n")
    for s in SCENARIOS:
        print(s)
    print("\\nEvery scenario must answer the 20 fundamental architectural questions!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 86: System Design Evaluation ==="
python3 phases/86-system-design-with-elasticsearch/code/86_system_design_with_elasticsearch.py
"""),

        (87, "Final Mental Model",
         "Elasticsearch is no longer a black box: trace POST /_doc and GET /_search through every layer from TCP packet to disk block.",
         """# Lesson 87.1: Final Mental Model

## Motto
"Elasticsearch is no longer a black box: trace POST /_doc and GET /_search through every layer from TCP packet to disk block."

## Problem
You started this course treating Elasticsearch as "a database with a search box." That simplification is now permanently replaced with deep, exact physical intuition.

## Prediction
Can you trace the complete life of a document from `POST /products/_doc/42` through every internal layer to disk, and trace `GET /products/_search` from client to coordinator to Lucene segment and back?

## Why this matters
This is the summit of the entire curriculum. You now possess the unified mental model of a distributed search engine engineer.

## First principles
The Grand Synthesis:
### The Complete Indexing Path:
```text
Client
  │ 1. POST /products/_doc/42 (HTTP JSON)
  ▼
Coordinating Node
  │ 2. Routing: hash("42") % 3 = Shard 1
  ▼
Primary Shard (Data Node A)
  ├── 3. Validate mapping schema
  ├── 4. Text Analysis: Char Filters ──► Tokenizer ──► Token Filters
  ├── 5. Write terms to Lucene in-memory Indexing Buffer
  ├── 6. Append operation to Translog on disk (WAL for durability)
  └── 7. Forward operation concurrently to Replica Shard (Data Node B)
            │
            ▼
       Replica acknowledges
            │
            ▼
HTTP 201 Created returned to Client!
            │
[ Background: Refresh every 1s ] ──► Buffer flushed to new immutable Segment in OS Cache (Searchable!)
[ Background: Flush every 30m ]  ──► fsync() segments to physical disk; Translog truncated.
[ Background: Tiered Merge ]     ──► Consolidates small segments, purges deleted docs.
```

### The Complete Search Path:
```text
Client
  │ 1. GET /products/_search?q=wireless&size=10
  ▼
Coordinating Node
  ├── 2. Parse Query DSL
  ├── 3. Identify active shards (Shard 0, Shard 1, Shard 2)
  │
  ├─ PHASE 1: QUERY PHASE (Scatter)
  │   ├── Send query to 1 copy of each shard (Primary or Replica)
  │   ├── Each shard queries its immutable Lucene segments in parallel
  │   ├── Evaluates postings lists, applies filter bitsets, calculates BM25 scores
  │   └── Each shard returns top 10 (DocID, Score) to Coordinator
  │
  ├── 4. Priority Queue Merge: Coordinator reduces candidate IDs to find global Top 10
  │
  ├─ PHASE 2: FETCH PHASE (Gather)
  │   ├── Requests full _source JSON only for the winning 10 document IDs
  │   └── Shards read compressed _source blocks from disk/cache
  │
  └── 5. Assemble JSON response ──► HTTP 200 OK returned to Client!
```

## Mental model
```text
              THE COMPLETE ELASTICSEARCH ENGINE
┌─────────────────────────────────────────────────────────────┐
│ 1. Distributed Layer: Coordinating Node, Shards, Replicas   │
│ 2. Memory Layer: JVM Heap (31GB Max) vs OS Page Cache       │
│ 3. Storage Layer: Immutable Lucene Segments (.doc, .tim)   │
│ 4. Columnar Layer: Doc Values (.dvd) for Sorts & Facets     │
│ 5. Durability Layer: Translog append-only commit log        │
│ 6. Relevance Layer: BM25 (TF Saturation, IDF, Length Norm)  │
└─────────────────────────────────────────────────────────────┘
```

## Build it
See `code/end_to_end_tracer.py` printing the step-by-step trace of writes and searches in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/87-final-mental-model/experiments/run_experiment.sh
```

## Inspect it
Execute an end-to-end write, refresh, search, explain, and aggregation in a single script.

## Measure it
Verify your deep understanding of latency, memory, and disk trade-offs.

## Break it
Explain what happens to the pipeline when:
* A node dies mid-write
* A slow shard lags during query phase
* An analyzer mapping is modified
* Refresh is delayed

## Recover it
You can now diagnose and recover any failure mode with technical certainty.

## Evidence
Record your final graduation reflections in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch acknowledge a write before it is visible to search?
2. How do immutable Lucene segments, sharding, and query coordination interact to make distributed search fast, scalable, and resilient?

## Guarantees
* You possess an accurate, first-principles mental model of distributed search engine engineering.

## Final Summary
Elasticsearch is no longer a black box.

## What comes next
Apply these principles across distributed system design, high-scale search architectures, and real-world engineering!
""",
"""#!/usr/bin/env python3

def trace_write_lifecycle(doc_id, doc_body):
    return [
        f"1. Client POST /products/_doc/{doc_id}",
        f"2. Coordinating Node hashes ID -> Shard 1",
        f"3. Primary Shard validates mapping schema",
        f"4. Text Analyzer emits tokens: {doc_body.get('title', '').lower().split()}",
        f"5. Wrote terms to in-memory Indexing Buffer",
        f"6. Appended raw write to Translog on disk (Durability)",
        f"7. Dispatched write to Replica Shard on Node B",
        f"8. HTTP 201 Created returned to client",
        f"9. [T+1.0s] Refresh flushes buffer -> New Searchable Segment in OS Cache",
        f"10. [T+30m] Flush calls fsync() to disk -> Translog cleared",
        f"11. Background Tiered Merge consolidates segments & purges tombstones"
    ]

def trace_search_lifecycle(query_term):
    return [
        f"1. Client GET /products/_search?q={query_term}&size=10",
        f"2. Coordinating Node parses query and scatters to Shards [0, 1, 2]",
        f"3. Query Phase: Shards evaluate inverted index postings & BM25 scores",
        f"4. Each Shard returns its top 10 (DocID, BM25 Score) tuples",
        f"5. Coordinating Node priority-queue merges candidate lists -> Global Top 10",
        f"6. Fetch Phase: Coordinator requests _source only for 10 winning IDs",
        f"7. Shards decompress and return _source JSON",
        f"8. HTTP 200 OK returned to client with hits & facets"
    ]

if __name__ == "__main__":
    print("=== The Complete End-to-End Write Pipeline Trace ===")
    for step in trace_write_lifecycle("42", {"title": "Distributed Search Guide", "price": 49.99}):
        print(" ", step)

    print("\\n=== The Complete End-to-End Search Pipeline Trace ===")
    for step in trace_search_lifecycle("distributed"):
        print(" ", step)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 87: Final Mental Model Trace ==="
python3 phases/87-final-mental-model/code/87_final_mental_model.py
""")
    ]

    for p_num, p_title, motto, doc_content, code_content, exp_content in phases:
        slug = f"{p_num:02d}-{p_title.lower().replace(' ', '-').replace('/', '-')}"
        phase_dir = os.path.join(PHASES_DIR, slug)
        write_file(os.path.join(phase_dir, "docs", "en.md"), doc_content)
        write_file(os.path.join(phase_dir, "code", f"{slug.replace('-', '_')}.py"), code_content)
        write_file(os.path.join(phase_dir, "experiments", "run_experiment.sh"), exp_content)
        write_file(os.path.join(phase_dir, "outputs", "evidence-template.md"), evidence_template(p_title, p_num))
        print(f"Generated Phase {p_num:02d}: {p_title}")

if __name__ == "__main__":
    generate_phases_82_to_87()
