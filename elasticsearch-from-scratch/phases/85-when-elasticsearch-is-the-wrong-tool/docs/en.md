# Lesson 85.1: When Elasticsearch Is the Wrong Tool

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
1. **Primary Key Point Lookups ($< 1$ ms):** Redis provides sub-millisecond in-memory lookups at $10	imes$ the throughput of Elasticsearch.
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
