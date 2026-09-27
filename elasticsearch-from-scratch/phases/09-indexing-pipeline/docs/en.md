# Lesson 09.1: Indexing Pipeline

## Motto
"From JSON to disk: parse, route, validate against mapping, analyze terms, append to translog, and write segment buffer."

## Problem
When a client issues `POST /orders/_doc/1`, what actually happens before HTTP 201 Created is returned? Treating this as an atomic database insert hides the dual write to the in-memory indexing buffer and durable transaction log (translog).

## Prediction
Does a successful HTTP 201 Created response mean the document is immediately searchable by concurrent queries?

## Why this matters
Understanding the write pipeline explains write amplification, translog durability, indexing backpressure, and why bulk indexing is drastically faster than individual document inserts.

## First principles
The write pipeline steps:
1. Client sends HTTP POST to any node (Coordinating Node).
2. Coordinating node computes shard: `hash(id) % num_shards`.
3. Request forwarded to Primary Shard node.
4. Primary parses JSON, validates against mapping schema.
5. Analysis pipeline transforms text into terms.
6. Writes to **In-Memory Indexing Buffer** (RAM).
7. Appends operation to **Translog** (disk for durability).
8. Replicates write concurrently to all active Replica Shards.
9. Once primary + replicas acknowledge, HTTP 200/201 response sent to client.

## Mental model
```text
Client
  │ 1. POST /index/_doc/42
  ▼
Coordinating Node
  │ 2. hash("42") % 3 = Shard 1
  ▼
Primary Shard (Node A)
  ├── 3. Parse & Validate Mapping
  ├── 4. Execute Analysis Pipeline
  ├── 5. Write to Lucene Index Buffer (RAM)
  ├── 6. Append to Translog (WAL on disk)
  └── 7. Send write to Replica Shard (Node B)
            │
            ▼
       Replica acknowledges
            │
            ▼
HTTP 201 Created to Client
```

## Build it
See `code/trace_indexing.py` simulating the step-by-step pipeline in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/09-indexing-pipeline/experiments/run_experiment.sh
```

## Inspect it
Inspect the translog generation and uncommitted operations:
```bash
curl -s http://localhost:9200/strict_products/_stats/translog?pretty
```

## Measure it
Measure single-document indexing latency under concurrency.

## Break it
Send invalid JSON or a document violating mapping types and inspect the rejected response.

## Recover it
Correct client payload to match mapping contract.

## Modify it
Toggle the translog sync policy between `request` (sync on every write) and `async` and measure throughput difference.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch write to BOTH an in-memory buffer and a disk translog during indexing?
2. If the node loses power before a refresh occurs, is the indexed document lost?

## Guarantees
* Acknowledged writes are recorded in the translog for crash durability.

## Non-guarantees
* Acknowledged writes are NOT immediately visible to search (until refresh).

## When to use this
* Every document write, update, or bulk ingestion operation.

## When not to use this
* Never use Elasticsearch as an ACID transactional ledger.

## What comes next
In Phase 10, we trace the opposite path: the search and query execution pipeline.
