# Lesson 54.1: High Cardinality

## Motto
"High cardinality fields have millions of unique values: aggregating on them strains doc values and coordinator memory."

## Problem
A query requests a `terms` aggregation on `session_uuid` across 50 million web events:
`"aggs": { "all_sessions": { "terms": { "field": "session_uuid", "size": 100000 } } }`
The query takes 25 seconds, transfers 100MB of bucket metadata per shard, and exhausts coordinator memory.

## Prediction
Why is a `terms` aggregation on `country` (cardinality ~200) vastly faster than a `terms` aggregation on `user_uuid` (cardinality 10,000,000)?

## Why this matters
**Cardinality** (the number of distinct unique values in a field) dictates aggregation memory consumption and network transfer size across shards.

## First principles
* **Low Cardinality (e.g. status: 5 values):** Shards compute 5 bucket counts, coordinator merges 5 buckets. Instant.
* **High Cardinality (e.g. UUID: millions of values):** Shards must evaluate and track millions of distinct string values in doc values and priority queues.
* Coordinator must merge massive candidate lists from all shards.

## Mental model
```text
Low Cardinality (country: 3 values):
  Shard 0: [US: 100, UK: 50, CA: 30] ──► Coordinator merges 3 numbers!

High Cardinality (user_id: 1,000,000 unique values):
  Shard 0: 1,000,000 bucket objects in RAM ──► Massive coordination bottleneck!
```

## Build it
See `code/cardinality_impact_sim.py` demonstrating memory scaling with unique value counts in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/54-high-cardinality/experiments/run_experiment.sh
```

## Inspect it
Test `cardinality` aggregation (HyperLogLog++) vs `terms` aggregation on high-cardinality values:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "approx_count": { "cardinality": { "field": "category" } }
  }
}'
```

## Measure it
Compare aggregation latency as field cardinality increases from 10 to 100,000 unique items.

## Break it
Request `terms` aggregation with `size: 100000` on a high-cardinality field and observe query latency degrade.

## Recover it
1. Use `cardinality` aggregation instead of `terms` if only the distinct count is needed.
2. Filter before aggregating to reduce candidate document count.

## Modify it
Tune `shard_size` to balance accuracy vs coordination memory.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is computing the count of unique values with `cardinality` aggregation faster than running a `terms` aggregation?
2. What does `shard_size` control during high-cardinality terms aggregations?

## Guarantees
* HyperLogLog++ cardinality aggregation runs in constant bounded memory regardless of item count.

## Non-guarantees
* High-cardinality `terms` aggregations cannot bypass the memory cost of building thousands of buckets.

## When to use this
* Aggregation performance tuning and schema cardinality auditing.

## When not to use this
* Grouping by high-cardinality identifiers across millions of records.

## What comes next
In Phase 55, we examine Hot Shards: diagnosing uneven distributed load.
