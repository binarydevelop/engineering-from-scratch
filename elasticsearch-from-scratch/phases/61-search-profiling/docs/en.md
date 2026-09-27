# Lesson 61.1: Search Profiling

## Motto
"The profile API is a microsecond x-ray: dissect Lucene query timing, Lucene scorers, and shard-level bottlenecks."

## Problem
Your query is slow, but you do not know *which specific clause* is causing the delay. Is it the boolean `must`, the geo filter, the phrase match, or the aggregation?

## Prediction
Can Elasticsearch break down query execution time per Lucene component (e.g. `TermQuery`, `BooleanQuery`, `PointRangeQuery`) down to nanoseconds?

## Why this matters
The `_profile` API breaks open the black box. It measures exact execution time for every Lucene query component across every shard.

## First principles
Profile breakdown fields:
* `type`: The underlying Lucene class (e.g. `TermQuery`, `BlockMaxConjunctionScorer`).
* `time_in_nanos`: Exact duration spent in that component.
* `breakdown`:
  * `create_weight`: Building query scoring weight.
  * `build_scorer`: Initializing posting iterators.
  * `next_doc`: Advancing iterator across matching documents.
  * `score`: Computing BM25 score.
  * `match`: Testing candidate match.

## Mental model
```text
Profile Output Tree:
BooleanQuery: 12.4ms
  ├── TermQuery (title: wireless): 2.1ms (score: 1.2ms, next_doc: 0.8ms)
  └── PointRangeQuery (price: [0 TO 100]): 0.3ms (BKD tree evaluation)
```

## Build it
See `code/profile_parser.py` parsing and summarizing verbose profile responses into readable tables in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/61-search-profiling/experiments/run_experiment.sh
```

## Inspect it
Run a search with `"profile": true`:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "profile": true,
  "query": {
    "bool": {
      "must": [{ "match": { "title": "keyboard" } }],
      "filter": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```

## Measure it
Compare nanoseconds spent in `score` vs `next_doc`.

## Break it
Run `"profile": true` in production during peak load: profiling instruments every Lucene method call and can slow down queries by 2x to 5x!

## Recover it
Only use `profile: true` during development, testing, and isolated staging environments.

## Modify it
Inspect aggregation profiling: `profile.shards[].aggregations`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does running `"profile": true` add significant execution overhead to a query?
2. What does high `next_doc` time indicate compared to high `score` time?

## Guarantees
* Profiling reveals exact nanosecond execution times for every Lucene sub-query.

## Non-guarantees
* The profile numbers reflect execution with profiling overhead attached, not clean production speed.

## When to use this
* Query optimization, dissecting complex boolean trees, and comparing query rewrite strategies.

## When not to use this
* Production customer traffic.

## What comes next
In Phase 62, we study Indexing Backpressure and queue saturation.
