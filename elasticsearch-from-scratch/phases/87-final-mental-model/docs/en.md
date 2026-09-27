# Lesson 87.1: Final Mental Model

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
