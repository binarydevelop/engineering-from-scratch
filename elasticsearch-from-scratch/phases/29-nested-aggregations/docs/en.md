# Lesson 29.1: Nested Aggregations

## Motto
"Aggregations compose hierarchically: buckets contain buckets, and leaf buckets compute metrics."

## Problem
You need to generate a breakdown report: "For every product category, show the top brands, and for each brand, show the average customer review rating and total revenue". Flat SQL group-bys require complex cube queries.

## Prediction
Can you nest a terms aggregation inside another terms aggregation, and then place a metric aggregation inside the inner terms aggregation?

## Why this matters
Hierarchical tree aggregations allow constructing OLAP cubes in a single distributed pass over Lucene doc values.

## First principles
Aggregation tree evaluation:
1. Root query selects candidate documents.
2. Parent bucket splits documents into groups ($A_1, A_2$).
3. Child bucket splits each parent bucket into subgroups ($B_{1,1}, B_{1,2}$).
4. Leaf metric computes statistical reduction on the sub-group.

## Mental model
```text
Root: All Products
  │
  ├── Bucket: Electronics
  │     ├── Sub-bucket: Brand Apple  ──► Avg Price: $999
  │     └── Sub-bucket: Brand Sony   ──► Avg Price: $499
  │
  └── Bucket: Furniture
        ├── Sub-bucket: Brand Herman ──► Avg Price: $1200
        └── Sub-bucket: Brand IKEA   ──► Avg Price: $150
```

## Build it
See `code/nested_agg_tree.py` simulating multi-tier aggregation trees in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/29-nested-aggregations/experiments/run_experiment.sh
```

## Inspect it
Execute a nested 2-tier bucket aggregation:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "by_category": {
      "terms": { "field": "category" },
      "aggs": {
        "avg_price": { "avg": { "field": "price" } },
        "max_price": { "max": { "field": "price" } }
      }
    }
  }
}'
```

## Measure it
Measure response payload size and execution time as nesting depth increases from 1 to 4 levels.

## Break it
Create a 5-level deep nested terms aggregation with `size: 100` on each level ($100^5 = 10,000,000,000$ buckets!) and observe the JVM memory breaker trip.

## Recover it
Limit nesting depth and keep bucket `size` small (e.g. 5 to 10).

## Modify it
Add a `date_histogram` parent bucket with `terms` children to analyze category trends over time.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does bucket cardinality multiply exponentially with each nested level?
2. What guardrail setting prevents runaway bucket explosions in Elasticsearch? (`search.max_buckets`)

## Guarantees
* Child aggregations are strictly scoped to the document subset of their parent bucket.

## Non-guarantees
* Deeply nested high-cardinality aggregations will exhaust coordinator heap memory.

## When to use this
* Multi-dimensional sales reports, category-brand-model trees, and log status breakdowns.

## When not to use this
* Deep combinatorial cross-tabulations across thousands of dimensions.

## What comes next
In Phase 30, we address the critical difference between standard flattened JSON objects and the `nested` field type.
