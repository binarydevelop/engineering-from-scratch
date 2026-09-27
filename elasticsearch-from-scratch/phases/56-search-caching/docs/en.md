# Lesson 56.1: Search Caching

## Motto
"Caches store bitsets and aggregation results, not whole HTTP payloads: understand Node Query Cache and Shard Request Cache."

## Problem
Engineers frequently assume Elasticsearch caches entire HTTP search responses like Redis or Varnish. When they see identical full-text queries taking 20ms every time, they wonder why "the cache is not working".

## Prediction
Does Elasticsearch cache the results of scored full-text queries, or only deterministic filter bitsets?

## Why this matters
Elasticsearch has sophisticated caching tiers. Knowing what is eligible for caching allows architecting queries for maximum cache reuse.

## First principles
The Two Primary Caches:
1. **Node Query Cache (Filter Cache):** Caches the matching document bitsets (Roaring Bitmaps) of clauses executed in **filter context**.
   * Only caches filters that run frequently (tracked by a frequency heuristic).
   * Per-segment bitset: if a segment does not change, its cached bitset remains valid forever!
2. **Shard Request Cache:** Caches local shard-level results of queries with `size: 0` (pure aggregations).
   * Automatically invalidated as soon as the shard is refreshed.

## Mental model
```text
Filter: "category: electronics"
  Segment _0 (Immutable) ──► Evaluated once ──► Bitset [1, 0, 1, 1...] cached in RAM!
  Next 1,000 queries ────► Bitwise AND in 0.001 ms! Zero Lucene index reads!
```

## Build it
See `code/filter_cache_sim.py` demonstrating bitset reuse in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/56-search-caching/experiments/run_experiment.sh
```

## Inspect it
Check cache hit and miss stats across nodes:
```bash
curl -s "http://localhost:9200/_nodes/stats/indices/query_cache,request_cache?pretty"
```

## Measure it
Measure latency of a repeated filter query on first run vs tenth run.

## Break it
Put non-deterministic terms like `now` in filters (`created_at >= now-1m`). Because `now` changes every millisecond, each query is unique and the cache misses 100% of the time!

## Recover it
Round timestamps using date math: `created_at >= now-1m/m`.

## Modify it
Explicitly enable or disable request caching: `"request_cache": true`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the Node Query Cache cache bitsets per Lucene segment rather than per index?
2. What invalidates the Shard Request Cache on a shard? (A refresh).

## Guarantees
* Unchanged segments retain their cached filter bitsets across query executions.

## Non-guarantees
* Scored queries in query context (`must`, `should`) are never cached in the Node Query Cache.

## When to use this
* Reusable categorical filters, status flags, and recurring dashboards.

## When not to use this
* Queries with high-precision unique timestamps (`now` without rounding).

## What comes next
In Phase 57, we contrast `from + size` with `search_after` for Deep Pagination.
