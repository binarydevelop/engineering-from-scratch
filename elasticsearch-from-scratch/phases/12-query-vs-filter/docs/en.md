# Lesson 12.1: Query vs Filter

## Motto
"Queries score relevance; filters ask binary existence. Filters can be cached; query scoring cannot."

## Problem
Running structured criteria (like `status: "ACTIVE"` or `created_at > 2026-01-01`) inside query context wastes CPU calculating BM25 relevance scores on fields where relevance is meaningless, while preventing Node Query Cache reuse.

## Prediction
Will a query clause returning hits have `_score: 0.0` when placed inside the `filter` block of a `bool` query?

## Why this matters
Filter context evaluates to a bitset (0 or 1). Elasticsearch caches frequent filter bitsets in the Node Query Cache (RAM). Next time the filter executes, it costs $O(1)$ bitwise AND operations instead of scanning Lucene indexes.

## First principles
* **Query Context:** "How well does this document match?" Relevance score is calculated via BM25. Cannot be cached as a bitset because score depends on query terms and document lengths.
* **Filter Context:** "Does this document match? Yes or No." Score is fixed at $0.0$. Candidate set is cached in memory as a Roaring Bitmap.

## Mental model
```text
Query Context:
  "title: wireless" ──► Compute BM25(tf, idf, len) ──► Score: 1.452 (Not Cacheable)

Filter Context:
  "price <= 100"    ──► Binary Check (True/False)   ──► Bitset [1, 0, 1, 1] ──► CACHED!
```

## Build it
See `code/query_vs_filter_bench.py` contrasting scoring overhead against binary filtering.

## Use Elasticsearch
Run the experiment:
```bash
./phases/12-query-vs-filter/experiments/run_experiment.sh
```

## Inspect it
Observe scores returned:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "bool": {
      "filter": [{ "term": { "category": "furniture" } }]
    }
  }
}'
```
Notice `_score: 0.0` for all hits.

## Measure it
Run repeated filter queries and inspect Node Query Cache hits via `_nodes/stats/indices/query_cache`.

## Break it
Put high-cardinality timestamps (`filter: { range: { timestamp: { gte: "now-1s" } } }`) in filters and observe cache churn.

## Recover it
Round timestamps to stable time buckets (e.g. `now/m` or `now/h`) so filter bitsets can be reused in cache.

## Modify it
Combine a scored `match` with two cached `filter` clauses.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch assign `_score: 0.0` to filter clauses?
2. How does the Node Query Cache decide which filter bitsets to keep in memory?

## Guarantees
* Filter clauses never alter document BM25 relevance ordering.

## Non-guarantees
* Putting a unique timestamp per request into a filter will not benefit from caching.

## When to use this
* Exact status flags, tenant IDs, date ranges, price filters, category facets.

## When not to use this
* When user search intent requires fuzzy, stemmed, or weighted ranking.

## What comes next
In Phase 13, we build relevance ranking from scratch, beginning with Term Frequency and Document Frequency.
