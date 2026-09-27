# Lesson 42.1: Sharding From First Principles

## Motto
"A shard is an independent Lucene index: partitioning allows an index to exceed the storage and compute of a single machine."

## Problem
A single node with a 2TB disk and 32GB RAM cannot hold a 10TB search corpus. Even if disk was infinite, a single CPU cannot process queries across 1 billion documents with sub-second latency.

## Prediction
Can an index with 3 primary shards be distributed across 3 distinct physical servers, with each server executing query work in parallel?

## Why this matters
Sharding is the horizontal scaling engine of Elasticsearch. Understanding that **a shard is literally an independent Apache Lucene index directory** demystifies distributed search.

## First principles
* **Index vs Shard:** An Index is a logical namespace; a Shard is a physical Lucene index instance.
* Sharding divides documents across $N$ primary shards.
* Adding nodes allows shards to spread out, distributing CPU, memory, and disk I/O.

## Mental model
```text
Logical Index: "logs-2026" (10 TB total)
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
 Shard 0    Shard 1    Shard 2
 (3.3 TB)   (3.3 TB)   (3.3 TB)
 [Node 1]   [Node 2]   [Node 3]
```

## Build it
See `code/shard_partition_sim.py` demonstrating hash partitioning of documents into distinct independent Lucene-like indices in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/42-sharding-from-first-principles/experiments/run_experiment.sh
```

## Inspect it
Create an index with 3 primary shards and inspect their physical assignment:
```bash
curl -X PUT http://localhost:9200/sharded_index -H "Content-Type: application/json" -d '{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 0
  }
}'
curl -s "http://localhost:9200/_cat/shards/sharded_index?v"
```

## Measure it
Inspect document distribution across the 3 shards using `_cat/shards`.

## Break it
Try to change `number_of_shards` from 3 to 4 on an existing index using `PUT /sharded_index/_settings`.
**Observed Error:** `"Cannot change primary shards for an open index."`

## Recover it
Primary shard count is immutable after index creation because document routing depends on the modulo of shard count! To change shard count, you must `_split`, `_shrink`, or create a new index and `_reindex`.

## Modify it
Inspect shard sizes on disk via `_cat/shards?v&h=index,shard,prirep,state,docs,store`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is a shard described as an "independent Lucene index"?
2. Why can you dynamically change `number_of_replicas` but NOT `number_of_shards`?

## Guarantees
* Sharding allows an index to store and query more data than can fit on any single physical server.

## Non-guarantees
* Adding more shards does not automatically make queries faster (fan-out coordination overhead).

## When to use this
* Scaling dataset storage and indexing capacity across multiple nodes.

## When not to use this
* Small datasets (< a few GB): a single primary shard is faster and consumes far less memory.

## What comes next
In Phase 43, we analyze Document Routing: how Elasticsearch decides which shard stores which document.
