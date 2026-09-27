# Lesson 46.1: Shard Count

## Motto
"More shards is not always faster: shard count is a capacity decision, not a performance dial."

## Problem
A team creates an index for 1 GB of data and configures 20 primary shards, assuming "more shards = more parallel threads = 20x faster search". In reality, queries become 3x slower and cluster metadata bloats!

## Prediction
Will a 50MB index search faster with 1 primary shard or with 10 primary shards?

## Why this matters
Sharding introduces overhead: thread context switches, network serialization, memory per segment, and coordinator reduce time.

## First principles
Rules of Thumb for Shard Sizing:
* **Recommended Shard Size:** 10 GB to 50 GB per shard for standard search; up to 50 GB for time-series logs.
* If your entire dataset is 2 GB, it belongs in **1 primary shard**!
* Each shard consumes JVM heap memory for segment dictionaries and open file descriptors.

## Mental model
```text
50 MB Dataset in 1 Shard:
  Coordinator ──► 1 Shard ──► Return Hits. (Zero Network Fan-Out, ~2ms)

50 MB Dataset in 20 Shards:
  Coordinator ──► 20 Shards ──► 20 TCP roundtrips ──► Coordinator merges 20 queues. (~15ms!)
```

## Build it
See `code/shard_count_bench.py` simulating fan-out latency scaling in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/46-shard-count/experiments/run_experiment.sh
```

## Inspect it
Compare search latency between an index with 1 shard vs 10 shards on identical data:
```bash
curl -X PUT http://localhost:9200/idx_1shard -H "Content-Type: application/json" -d '{"settings": {"number_of_shards": 1, "number_of_replicas": 0}}'
curl -X PUT http://localhost:9200/idx_10shards -H "Content-Type: application/json" -d '{"settings": {"number_of_shards": 10, "number_of_replicas": 0}}'
```

## Measure it
Benchmark query latency on both indices and observe that 1 shard outperforms 10 shards on small data.

## Break it
Create 1,000 tiny shards in a test cluster and observe cluster state sync lag and JVM heap consumption.

## Recover it
Use `_shrink` API or Reindex to consolidate into fewer, properly sized shards.

## Modify it
Calculate target shard count based on expected annual data volume.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an index with 20 primary shards perform worse on small datasets than an index with 1 shard?
2. What is the generally recommended shard size range in production?

## Guarantees
* A single shard eliminates all distributed scatter-gather coordination overhead.

## Non-guarantees
* A single shard cannot scale beyond the physical storage limit of one server.

## When to use this
* Capacity planning and initial index architecture.

## When not to use this
* Blindly accepting defaults without calculating data volume.

## What comes next
In Phase 47, we examine the production disaster of Oversharding.
