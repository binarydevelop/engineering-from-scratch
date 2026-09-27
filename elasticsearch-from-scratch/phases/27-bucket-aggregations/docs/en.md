# Lesson 27.1: Bucket Aggregations

## Motto
"Bucket aggregations partition documents into sets: terms, ranges, date histograms, and filters."

## Problem
How do you build e-commerce sidebar filters (Category: Shoes (42), Electronics (88); Price: $0-$50 (12), $50-$100 (34)) without running dozens of separate count queries?

## Prediction
What happens if you run a `terms` aggregation on a field with 10 million distinct values?

## Why this matters
Bucket aggregations do not calculate single metrics; they partition the entire document stream into buckets based on criteria.

## First principles
Major bucket aggregations:
* `terms`: Groups by unique keyword values (e.g. status, category).
* `date_histogram`: Slices continuous timestamps into calendar buckets (`1d`, `1h`, `1m`).
* `range`: Divides numeric fields into custom user intervals.
* `filter`: Creates a custom bucket matching a specific sub-query.

## Mental model
```text
All Documents (1,000 items)
          │
  [ Terms Aggregation on 'category' ]
          │
   ┌──────┴──────┐
   ▼             ▼
Bucket: Tech   Bucket: Home
Count: 650     Count: 350
```

## Build it
See `code/bucket_aggs.py` simulating terms and range bucketing in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/27-bucket-aggregations/experiments/run_experiment.sh
```

## Inspect it
Execute terms and range bucket aggregations:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "by_category": { "terms": { "field": "category" } },
    "price_ranges": {
      "range": {
        "field": "price",
        "ranges": [
          { "to": 100 },
          { "from": 100, "to": 250 },
          { "from": 250 }
        ]
      }
    }
  }
}'
```

## Measure it
Measure latency when aggregating 10 buckets vs 1,000 buckets.

## Break it
Run a `terms` aggregation on a high-cardinality analyzed `text` field without doc values and observe the immediate rejection.

## Recover it
Aggregate against `.keyword` multi-fields backed by doc values.

## Modify it
Use `date_histogram` with `fixed_interval: "1h"`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does a distributed terms aggregation calculate approximate counts across shards?
2. What parameter controls the candidate buffer size per shard during terms aggregation? (`shard_size`)

## Guarantees
* Every matching document is assigned to matching buckets deterministically.

## Non-guarantees
* Top-$N$ terms aggregation across hundreds of shards is approximate unless `size` is equal to total cardinality.

## When to use this
* Faceted search, histograms, time-series bucketing, and categorizations.

## When not to use this
* Primary key unique ID extraction.

## What comes next
In Phase 28, we explore Metric Aggregations (`avg`, `sum`, `cardinality`).
