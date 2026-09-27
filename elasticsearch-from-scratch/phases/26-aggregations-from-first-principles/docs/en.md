# Lesson 26.1: Aggregations From First Principles

## Motto
"Search finds candidate documents; aggregations reduce candidate fields into statistical summaries."

## Problem
Users want more than a list of matching items. In e-commerce, they want: "Show me matching items, AND tell me how many are in electronics vs furniture, AND show the average price in each category". Executing separate database queries for every facet causes severe query amplification.

## Prediction
Can Elasticsearch return both full-text search hits AND analytical aggregations in a single HTTP request?

## Why this matters
Elasticsearch is not only a search engine; it is a distributed analytics engine. Aggregations run concurrently across shards during query execution.

## First principles
The dual execution model:
* **Hits Pipeline:** Collects and ranks the top $K$ document bodies.
* **Aggregations Pipeline:** Iterates through ALL matching document IDs in the candidate set and updates running statistical accumulators (counts, sums, histograms) using columnar **Doc Values**.
* If `size: 0` is passed, the hits retrieval is skipped completely, executing pure analytics!

## Mental model
```text
Query: "wireless" ──► Candidate Set: [Doc 1, Doc 4, Doc 7, Doc 12]
                              │
         ┌────────────────────┴────────────────────┐
         ▼                                         ▼
   HITS PIPELINE                             AGGS PIPELINE
  Top 10 winning docs                      Iterate doc values:
  [Doc 1, Doc 4]                           - category counts: {tech: 3, home: 1}
  (Returns JSON _source)                   - avg price: $78.50
```

## Build it
See `code/map_reduce_aggs.py` implementing map-reduce style bucketing and metrics in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/26-aggregations-from-first-principles/experiments/run_experiment.sh
```

## Inspect it
Issue a search query requesting both hits and category term facets:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 1,
  "query": { "match_all": {} },
  "aggs": {
    "categories": { "terms": { "field": "category" } }
  }
}'
```

## Measure it
Compare execution time with `size: 10` versus `size: 0`.

## Break it
Run an aggregation across an empty index or on an unmapped field.

## Recover it
Ensure field exists in the mapping as `keyword` or numeric point.

## Modify it
Add a sub-aggregation computing the average price per category.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does setting `"size": 0` improve aggregation performance?
2. What underlying data structure makes iterating millions of field values fast without loading full documents?

## Guarantees
* Aggregations evaluate all documents that satisfy the query clause.

## Non-guarantees
* Terms aggregations on high-cardinality distributed shards can be slightly approximate unless `shard_size` is tuned.

## When to use this
* Faceted navigation, metrics dashboards, log summaries, and business intelligence.

## When not to use this
* Complex multi-table relational joins (use OLAP warehouses like ClickHouse or BigQuery).

## What comes next
In Phase 27, we study Bucket Aggregations in depth.
