# Lesson 82.1: Elasticsearch vs Database (PostgreSQL)

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
