# Lesson 10.1: Search Pipeline

## Motto
"Search is an inverted index scan across immutable segments, scored by relevance and reduced at the coordinator."

## Problem
How does Elasticsearch execute a query across multiple shards and millions of documents in 5 milliseconds? Without understanding the two-phase query pipeline, performance tuning is guesswork.

## Prediction
When you ask for `size: 10` on a 5-shard index, do shards send 10 documents each to the coordinator, or do they send full document bodies immediately?

## Why this matters
The query pipeline separates candidate matching and scoring from full document retrieval, minimizing network traffic across cluster nodes.

## First principles
Search executes in two phases:
1. **Query Phase:** Coordinating node scatters query to shards. Each shard queries its Lucene segments, scores matches using BM25, and returns a priority queue of candidate IDs + scores (e.g. top 10).
2. **Fetch Phase:** Coordinating node merges shard queues to find global top 10 winners, then requests full `_source` bodies only for those 10 winning IDs.

## Mental model
```text
                      COORDINATING NODE
                             │
     ┌───────────────────────┴───────────────────────┐
     │ 1. Scatter Query (No docs transferred)        │
     ▼                                               ▼
  SHARD 0                                         SHARD 1
- Postings lookup                               - Postings lookup
- BM25 score                                    - BM25 score
- Returns [Doc 4: 3.2, Doc 9: 2.8]              - Returns [Doc 1: 4.1, Doc 3: 1.5]
     │                                               │
     └───────────────────────┬───────────────────────┘
                             ▼
  2. Merge Top Hits: Overall Winners = [Doc 1 (4.1), Doc 4 (3.2)]
                             │
  3. Fetch Phase: Request full _source only for Doc 1 & Doc 4
                             ▼
  4. Assemble Response -> Send to Client
```

## Build it
See `code/search_pipeline_trace.py` demonstrating query vs fetch phase in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/10-search-pipeline/experiments/run_experiment.sh
```

## Inspect it
Use the `_search` explain parameter to trace term matching and scoring:
```bash
curl -X POST http://localhost:9200/trace_demo/_search?explain=true -H "Content-Type: application/json" -d '{
  "query": { "match": { "msg": "trace" } }
}'
```

## Measure it
Measure query latency with `took` in the response payload.

## Break it
Request `size: 10000` with deep `from: 50000` and observe coordinator memory and network spike.

## Recover it
Switch to `search_after` with Point-in-Time (covered in Phase 57 & 58).

## Modify it
Add `_source: ["msg"]` to request only specific fields during the fetch phase and measure payload size reduction.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch not fetch `_source` during the query phase?
2. What is the network overhead of querying 100 shards versus 2 shards?

## Guarantees
* Query-then-fetch guarantees globally accurate top-$K$ relevance ranking across all shards.

## Non-guarantees
* Exact total hit counts above 10,000 are approximate by default (`relation: "gte"`).

## When to use this
* Standard full-text search and analytical querying.

## When not to use this
* Bulk export of millions of raw records (use Scroll API or sliced `search_after`).

## What comes next
In Phase 11, we explore compound search with Boolean queries (`must`, `filter`, `should`, `must_not`).
