# Lesson 47.1: Oversharding

## Motto
"Thousands of tiny shards cause death by a thousand cuts: heap exhaustion, thread contention, and slow recovery."

## Problem
A company creates daily indices with 5 primary shards and 1 replica for each microservice. After 2 years, the cluster hosts 15,000 shards across only 3 nodes (averaging 5,000 shards per node!). The cluster master freezes, searches time out, and nodes crash with OutOfMemory errors.

## Prediction
Why does each Lucene shard consume JVM heap memory even when it receives zero search and write traffic?

## Why this matters
Oversharding is the #1 cause of unprovoked Elasticsearch cluster instability.

## First principles
The Cost of a Shard:
1. **JVM Heap:** Each shard holds open Lucene segment metadata, FST term dictionaries, and doc values readers in memory (approx 10MB to 50MB of heap per shard, even if empty!).
2. **File Descriptors:** Each shard holds dozens of open file handles on disk.
3. **Master Coordination:** The active master node must broadcast the status of every single shard in the cluster state. A 100MB cluster state payload causes network partitions and master election loops.
4. **Thread Contention:** A search across 2,000 shards overwhelms search thread pool queues.

## Mental model
```text
Healthy Cluster:
  30 Shards (30GB each) ──► Low Heap, Low Thread Contention, Instant Recovery

Oversharded Cluster:
  3,000 Shards (30MB each) ──► 3,000 Lucene directories in memory ──► CLUSTER COLLAPSE!
```

## Build it
See `code/oversharding_calculator.py` estimating heap memory consumption per shard count in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/47-oversharding/experiments/run_experiment.sh
```

## Inspect it
Check your cluster's total shard count per node:
```bash
curl -s "http://localhost:9200/_cat/nodes?v&h=name,node.role,shards,heap.percent"
```

## Measure it
Observe the guideline: maintain **under 20 shards per GB of JVM heap** on any data node.

## Break it
Inspect cluster health when shard limits are approached (`cluster.max_shards_per_node`, default 1,000 in modern ES).

## Recover it
1. Delete obsolete indices.
2. Shrink indices via `_shrink`.
3. Consolidate daily indices into monthly indices via `_reindex`.
4. Implement Index Lifecycle Management (ILM, Phase 66).

## Modify it
Calculate optimal shard allocation for a 500GB logging cluster.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an empty shard consume JVM heap memory?
2. What is the recommended maximum ratio of shards to JVM heap gigabytes?

## Guarantees
* Limiting shard count preserves master node responsiveness and keeps cluster state compact.

## Non-guarantees
* Shard limits alone cannot prevent OOM if individual aggregations exceed heap memory.

## When to use this
* Cluster health auditing, capacity reviews, and architectural sizing.

## When not to use this
* Ignoring shard counts until the cluster turns red.

## What comes next
In Phase 48, we study Replicas and their role in High Availability.
