# Lesson 28.1: Metric Aggregations

## Motto
"Metric aggregations compute mathematical reductions over doc values: min, max, avg, percentiles, and HyperLogLog cardinality."

## Problem
Computing statistical metrics across 50,000,000 logs (e.g. 99th percentile API latency or unique visitors count) in memory would crash the JVM heap if all values had to be collected into sets.

## Prediction
Does the `cardinality` aggregation store every unique string in memory, or does it use a probabilistic algorithm?

## Why this matters
Elasticsearch implements single-value and multi-value metric aggregations, including **HyperLogLog++** for constant-memory cardinality estimation and **T-Digest** for streaming percentiles.

## First principles
* **Exact Metrics:** `min`, `max`, `sum`, `avg`, `value_count`. Computed by accumulator state during doc values scan.
* **Approximate Metrics:**
  * `cardinality`: Uses HyperLogLog++ algorithm. Provides bounded memory footprint (< a few KB) with tunable precision threshold.
  * `percentiles`: Uses T-Digest quantile compression algorithm.

## Mental model
```text
10,000,000 User IDs:
  Exact Set: 10M * 36 bytes UUID ≈ 360 MB JVM Heap
  HyperLogLog++: Registers bit sketch ≈ 8 KB Fixed Memory (Approx error < 1%)
```

## Build it
See `code/metrics_simulation.py` demonstrating exact vs streaming accumulators in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/28-metric-aggregations/experiments/run_experiment.sh
```

## Inspect it
Run `stats`, `percentiles`, and `cardinality` aggregations:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "price_stats": { "stats": { "field": "price" } },
    "price_percentiles": { "percentiles": { "field": "price", "percents": [50, 95, 99] } },
    "unique_categories": { "cardinality": { "field": "category" } }
  }
}'
```

## Measure it
Measure execution time of `stats` across thousands of documents.

## Break it
Increase `precision_threshold` on `cardinality` aggregation to 40,000 and observe heap usage.

## Recover it
Use default `precision_threshold: 3000` (provides high accuracy for normal cardinality counts with negligible heap).

## Modify it
Use `extended_stats` to inspect standard deviation and variance.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch use HyperLogLog++ for the `cardinality` aggregation?
2. What is the difference between single-value metrics (`avg`) and multi-value metrics (`stats`)?

## Guarantees
* Linear arithmetic metrics (`sum`, `avg`, `min`, `max`) are mathematically exact.

## Non-guarantees
* Cardinality and percentiles are probabilistic estimates within bounded error rates.

## When to use this
* Real-time metrics dashboards, SLA monitoring, and KPI calculations.

## When not to use this
* Financial auditing that requires provably 100% exact unique entity reconciliations.

## What comes next
In Phase 29, we nest aggregations to build multi-dimensional analytics.
