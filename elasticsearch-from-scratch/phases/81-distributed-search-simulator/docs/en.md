# Lesson 81.1: Distributed Search Simulator

## Motto
"Build a distributed cluster simulator in Python: 1 coordinator node, 3 shard workers, and simulated network partitions."

## Problem
How does a coordinating node handle a shard timing out, a node crashing mid-query, or uneven response latencies across a cluster? Testing this on real production clusters is risky; building a multi-worker simulator makes the distributed dynamics crystal clear.

## Prediction
What happens to total query latency when 2 shards respond in 5ms, but the 3rd shard experiences a 500ms network lag?

## Why this matters
Simulating the coordinator-shard interaction cements your mental model of scatter-gather, fan-out, partial hits, and cluster consensus.

## First principles
Distributed Simulator Architecture:
* **Shard Workers (3 instances):** Each worker maintains its own isolated inverted index and doc values.
* **Coordinator:**
  1. Computes shard routing for writes (`hash(id) % 3`).
  2. Scatters queries in parallel to all 3 workers.
  3. Priority-queue merges top hits.
  4. Detects worker timeouts and reports `timed_out: true` or partial hits.

## Mental model
```text
                     COORDINATOR WORKER
                              │
     ┌────────────────────────┼────────────────────────┐
     │ Query (async)          │ Query (async)          │ Query (async)
     ▼                        ▼                        ▼
  SHARD 0                  SHARD 1                  SHARD 2
  (Fast: 3ms)              (Fast: 4ms)              (Slow: 250ms)
     │                        │                        │
     └────────────────────────┼────────────────────────┘
                              ▼
            Coordinator waits for Shard 2!
            Total latency = max(3ms, 4ms, 250ms) = 250ms!
```

## Build it
See `projects/distributed_simulator/` and `code/distributed_simulator.py` implementing the complete coordinator and shard workers in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/81-distributed-search-simulator/experiments/run_experiment.sh
```

## Inspect it
Observe simulated scatter-gather query execution across the 3 shard workers.

## Measure it
Benchmark total query latency with and without slow shard injection.

## Break it
Simulate a dead shard worker: observe coordinator handling partial hit responses (`_shards.failed: 1`).

## Recover it
Implement timeout thresholds (`timeout: "50ms"`) so queries return partial results rather than blocking indefinitely.

## Modify it
Add replica shard worker fallbacks.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is distributed search latency always bounded by the slowest participating shard?
2. What does Elasticsearch return in the HTTP response if one shard fails during query execution?

## Guarantees
* Demonstrates the exact network coordination dynamics of distributed search engines.

## Non-guarantees
* Does not implement full Raft distributed consensus for cluster state.

## When to use this
* Distributed systems education, latency modeling, and fault tolerance studies.

## When not to use this
* Production search serving.

## What comes next
In Phase 82, we compare Elasticsearch directly against PostgreSQL.
