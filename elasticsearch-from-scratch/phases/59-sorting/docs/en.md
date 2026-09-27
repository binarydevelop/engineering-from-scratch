# Lesson 59.1: Sorting

## Motto
"Relevance sort evaluates BM25; field sorting bypasses BM25 completely to read columnar doc values."

## Problem
When users sort by `price: asc` or `date: desc`, calculating BM25 relevance scores for millions of documents is pure wasted CPU.

## Prediction
Does sorting by an explicit field disable BM25 relevance scoring by default?

## Why this matters
Sorting by non-relevance criteria can be drastically optimized using Lucene's index-sorting and columnar doc values.

## First principles
* **Relevance Sort (`_score: desc`):** BM25 score must be computed for every candidate document.
* **Field Sort (`price: asc`):** Score calculation is bypassed completely (`_score: null`). Shards read contiguous values directly from columnar Doc Values.
* **Index Sorting:** Pre-sorting documents on disk at segment-write time (e.g. sort segment by `created_at desc`). Allows queries sorting by `created_at` to terminate early after reading the first $K$ hits!

## Mental model
```text
Relevance Sort:
  Query ──► Compute BM25 for all 100k hits ──► Sort by score ──► Return top 10

Field Sort on Doc Values:
  Query ──► Read Price column directly from disk cache ──► Return top 10 (Zero BM25 math!)

Index Sorted Segment:
  Segment pre-sorted by date ──► Read first 10 items off disk ──► EARLY TERMINATION! (Instant!)
```

## Build it
See `code/sorting_bench.py` demonstrating doc values sort vs scored sort in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/59-sorting/experiments/run_experiment.sh
```

## Inspect it
Sort by price and inspect the response:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": { "match_all": {} },
  "sort": [{ "price": "asc" }]
}'
```
Notice `_score: null` in the returned hits!

## Measure it
Compare query latency: sorting by `_score` vs sorting by an indexed numeric field.

## Break it
Sort on an analyzed `text` field without a keyword subfield:
`"Field [title] of type [text] does not support sorting. Use keyword multi-field."`

## Recover it
Sort on `title.keyword` backed by doc values.

## Modify it
Configure index-time sorting in index settings (`"index.sort.field": "created_at"`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does explicit field sorting set `_score: null` by default?
2. How does Index Sorting allow early termination during query execution?

## Guarantees
* Field sorting on doc values scales independently of document text length.

## Non-guarantees
* Sorting on unindexed or dynamic scripting expressions will degrade performance.

## When to use this
* Filtering products by price, news by timestamp, or logs by severity.

## When not to use this
* Pure relevance search where user intent depends on term match quality.

## What comes next
In Phase 60, we diagnose and mitigate Slow Queries.
