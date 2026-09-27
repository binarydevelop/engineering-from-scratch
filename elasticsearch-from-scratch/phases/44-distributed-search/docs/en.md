# Lesson 44.1: Distributed Search

## Motto
"Distributed search is scatter-gather: the coordinator broadcasts to every shard, gathers top hits, and merges the global result."

## Problem
When an index is split across 50 shards on 20 servers, how does a client obtain a globally sorted top-10 result list without transferring all documents across the network?

## Prediction
What happens if one shard out of 50 is slow or unresponsive during a scatter-gather search?

## Why this matters
Distributed search coordination introduces network latency, serialization overhead, and tail-latency sensitivity (the slow-shard problem).

## First principles
Scatter-Gather Protocol:
1. **Scatter:** Coordinating node sends lightweight query payload to one copy (primary or replica) of every shard in the index.
2. **Local Execution:** Each shard executes the query locally against its Lucene segments, computing local BM25 scores.
3. **Local Top-$K$:** Each shard returns its top $K$ candidate document IDs + scores.
4. **Gather & Merge:** Coordinating node priority-queue merges all shard results to determine the true global top $K$ winners.
5. **Fetch:** Coordinator requests `_source` only for winning IDs.

## Mental model
```text
                     CLIENT
                       │ GET /search?size=10
                       ▼
               COORDINATING NODE
             /         │               Scatter          Scatter    Scatter
           ▼           ▼           ▼
       Shard 0      Shard 1     Shard 2
       (Top 10)     (Top 10)    (Top 10)
           \           │           /
        Gather       Gather      Gather
             \         │         /
               COORDINATING NODE
          Priority Queue: Merge 30 items
          ──► Select Global Top 10
                       │
                       ▼
                     CLIENT
```

## Build it
See `code/scatter_gather_sim.py` simulating multi-shard query coordination and merging in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/44-distributed-search/experiments/run_experiment.sh
```

## Inspect it
Observe shard execution metadata in the search response header:
```json
"_shards": {
  "total": 3,
  "successful": 3,
  "skipped": 0,
  "failed": 0
}
```

## Measure it
Measure search latency as shard count increases from 1 to 20 for the exact same dataset size.

## Break it
Simulate a slow shard by injecting latency on one node; observe how total request latency is bounded by the slowest shard.

## Recover it
Inspect `_cat/thread_pool/search` and optimize shard allocations.

## Modify it
Pass `preference=_local` or `preference=_shards:0,1` to target specific shard subsets.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is distributed search latency dictated by the slowest participating shard?
2. What is the fan-out network cost when an index has 100 primary shards?

## Guarantees
* The coordinator produces an accurately merged top-$K$ result across all participating shards.

## Non-guarantees
* Having more shards does NOT automatically decrease search latency.

## When to use this
* Standard distributed search across multi-shard indices.

## When not to use this
* When oversharding creates hundreds of tiny shards with near-zero data.

## What comes next
In Phase 45, we examine the mechanics of the Query-Then-Fetch protocol.
