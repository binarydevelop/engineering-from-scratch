# Lesson 24.1: Numeric and Date Fields

## Motto
"Numbers and dates do not belong in inverted indexes: BKD trees provide O(log N) multi-dimensional range queries."

## Problem
Inverted indexes excel at finding exact terms (`"status: active"`). But for range queries (`price BETWEEN 50 AND 100` or `date >= 2026-01-01`), an inverted index must evaluate every single discrete number in the range, creating thousands of boolean clauses!

## Prediction
How does Lucene physically organize numbers on disk to make range queries fast?

## Why this matters
Elasticsearch uses **BKD Trees** (Block K-d Trees, point fields: `integer`, `long`, `float`, `double`, `date`) for numeric range queries.

## First principles
A **BKD Tree** is a space-partitioning binary tree that recursively divides multidimensional coordinate spaces:
* Leaf nodes store compact blocks of numeric points.
* A range query tests the bounding box of the tree node:
  * Node completely inside range $	o$ add all documents in leaf instantly.
  * Node completely outside range $	o$ skip entire branch.
  * Node intersects range boundary $	o$ recurse down children.

## Mental model
```text
                     [0 to 1000]
                    /                        [0 to 500]       [501 to 1000]
             /                 [0 to 250]  [251 to 500]
Range Query: price >= 600
  ──► Skips left half [0 to 500] in O(1) time!
```

## Build it
See `code/bkd_tree_sim.py` demonstrating recursive 1D range partitioning in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/24-numeric-and-date-fields/experiments/run_experiment.sh
```

## Inspect it
Create an index with numeric and date fields and issue a range query:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "query": {
    "range": {
      "price": { "gte": 50, "lte": 200 }
    }
  }
}'
```

## Measure it
Compare range query speed on a numeric field vs an un-indexed text string.

## Break it
Store a price as a string (`"price": "149.99"`) and run a string range query: `"149.99"` comes before `"50.00"` lexicographically!

## Recover it
Map the field as `double` or `scaled_float`.

## Modify it
Use date math syntax: `"gte": "now-7d/d"`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why are BKD trees superior to inverted indexes for continuous range queries?
2. What is `scaled_float` and when is it preferred over `double`?

## Guarantees
* Point fields provide logarithmic time range evaluations.

## Non-guarantees
* Continuous point fields do not support standard text tokenization or stemming.

## When to use this
* Prices, timestamps, latency metrics, counts, and geographic coordinates.

## When not to use this
* Categorical IDs that are only queried for exact equality (use `keyword` instead).

## What comes next
In Phase 25, we explore Geo Search (points, bounding boxes, and distance calculations).
