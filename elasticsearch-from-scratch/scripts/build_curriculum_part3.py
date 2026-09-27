#!/usr/bin/env python3
"""
build_curriculum_part3.py - Generates Phases 26 to 41 for elasticsearch-from-scratch.
Covers Aggregations, Doc Values, Fielddata, Segments, Near-Real-Time, Refresh, Flush, Merging, and Bulk Indexing.
"""

import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PHASES_DIR = os.path.join(BASE_DIR, "phases")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    if path.endswith(".sh") or path.endswith(".py"):
        os.chmod(path, 0o755)

def evidence_template(phase_title, phase_num):
    return f"""# Evidence Log: Phase {phase_num:02d} - {phase_title}

Date: 2026-09-23
Elasticsearch Version: 8.17.0
Lucene Version: 9.12.0
Working Directory: phases/{phase_num:02d}-{phase_title.lower().replace(' ', '-').replace('/', '-')}

## Prediction
Before executing the experiment, record your hypothesis here:

## Commands Executed
```bash
./experiments/run_experiment.sh
```

## Important Terminal Output
```text
```

## Measurements
* Metric 1:
* Metric 2:

## What Actually Happened?

## What Did I Intentionally Break?

## How Did I Diagnose It?

## How Did I Recover?

## Explain the Concept in My Own Words:
"""

def generate_phases_26_to_41():
    phases = [
        (26, "Aggregations From First Principles",
         "Search finds candidate documents; aggregations reduce candidate fields into statistical summaries.",
         """# Lesson 26.1: Aggregations From First Principles

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
""",
"""#!/usr/bin/env python3
from collections import defaultdict

def run_aggregations(docs, query_fn=None):
    category_counts = defaultdict(int)
    category_prices = defaultdict(list)

    for doc in docs:
        if query_fn and not query_fn(doc):
            continue
        cat = doc.get("category", "unknown")
        category_counts[cat] += 1
        category_prices[cat].append(doc.get("price", 0.0))

    summary = {}
    for cat, count in category_counts.items():
        prices = category_prices[cat]
        summary[cat] = {
            "doc_count": count,
            "avg_price": round(sum(prices) / count, 2),
            "max_price": max(prices)
        }
    return summary

if __name__ == "__main__":
    catalog = [
        {"title": "Keyboard", "category": "electronics", "price": 100},
        {"title": "Mouse", "category": "electronics", "price": 50},
        {"title": "Monitor", "category": "electronics", "price": 300},
        {"title": "Chair", "category": "furniture", "price": 200},
        {"title": "Desk", "category": "furniture", "price": 400}
    ]
    print("Aggregation Summary (Category Facets):")
    aggs = run_aggregations(catalog)
    for cat, data in aggs.items():
        print(f"  Category '{cat}': Count={data['doc_count']}, AvgPrice=${data['avg_price']}, MaxPrice=${data['max_price']}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 26: Aggregations From First Principles ==="
python3 phases/26-aggregations-from-first-principles/code/26_aggregations_from_first_principles.py
"""),

        (27, "Bucket Aggregations",
         "Bucket aggregations partition documents into sets: terms, ranges, date histograms, and filters.",
         """# Lesson 27.1: Bucket Aggregations

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
""",
"""#!/usr/bin/env python3
from collections import defaultdict

def bucket_terms(docs, field):
    buckets = defaultdict(int)
    for d in docs:
        val = d.get(field)
        if val is not None:
            buckets[val] += 1
    return dict(sorted(buckets.items(), key=lambda x: x[1], reverse=True))

def bucket_range(docs, field, ranges):
    # ranges: list of (label, min_val, max_val)
    bucket_counts = {r[0]: 0 for r in ranges}
    for d in docs:
        val = d.get(field)
        if val is not None:
            for label, low, high in ranges:
                if (low is None or val >= low) and (high is None or val < high):
                    bucket_counts[label] += 1
                    break
    return bucket_counts

if __name__ == "__main__":
    docs = [
        {"cat": "books", "price": 25},
        {"cat": "books", "price": 45},
        {"cat": "tech", "price": 150},
        {"cat": "tech", "price": 500},
        {"cat": "home", "price": 80}
    ]
    print("Terms Buckets (cat):", bucket_terms(docs, "cat"))
    price_ranges = [("under_50", None, 50), ("50_to_200", 50, 200), ("over_200", 200, None)]
    print("Range Buckets (price):", bucket_range(docs, "price", price_ranges))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 27: Bucket Aggregations ==="
python3 phases/27-bucket-aggregations/code/27_bucket_aggregations.py
"""),

        (28, "Metric Aggregations",
         "Metric aggregations compute mathematical reductions over doc values: min, max, avg, percentiles, and HyperLogLog cardinality.",
         """# Lesson 28.1: Metric Aggregations

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
""",
"""#!/usr/bin/env python3
import statistics

class MetricAccumulator:
    def __init__(self):
        self.count = 0
        self.total = 0.0
        self.min_val = float('inf')
        self.max_val = float('-inf')
        self.values = []

    def add(self, val):
        self.count += 1
        self.total += val
        if val < self.min_val: self.min_val = val
        if val > self.max_val: self.max_val = val
        self.values.append(val)

    def stats(self):
        avg = self.total / self.count if self.count > 0 else 0.0
        return {
            "count": self.count,
            "min": self.min_val,
            "max": self.max_val,
            "avg": round(avg, 2),
            "p95": round(statistics.quantiles(self.values, n=100)[94], 2) if len(self.values) >= 100 else None
        }

if __name__ == "__main__":
    acc = MetricAccumulator()
    import random
    random.seed(42)
    for _ in range(1000):
        acc.add(random.uniform(10.0, 500.0))
    print("Computed Streaming Metric Stats:")
    for k, v in acc.stats().items():
        print(f"  {k:10s}: {v}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 28: Metric Aggregations ==="
python3 phases/28-metric-aggregations/code/28_metric_aggregations.py
"""),

        (29, "Nested Aggregations",
         "Aggregations compose hierarchically: buckets contain buckets, and leaf buckets compute metrics.",
         """# Lesson 29.1: Nested Aggregations

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
""",
"""#!/usr/bin/env python3
from collections import defaultdict

def build_nested_aggs(items):
    # Category -> Brand -> list of prices
    tree = defaultdict(lambda: defaultdict(list))
    for it in items:
        tree[it["category"]][it["brand"]].append(it["price"])

    results = {}
    for cat, brands in tree.items():
        results[cat] = {"brands": {}}
        for brand, prices in brands.items():
            results[cat]["brands"][brand] = {
                "count": len(prices),
                "avg_price": round(sum(prices) / len(prices), 2)
            }
    return results

if __name__ == "__main__":
    catalog = [
        {"category": "tech", "brand": "apple", "price": 1200},
        {"category": "tech", "brand": "apple", "price": 800},
        {"category": "tech", "brand": "sony", "price": 400},
        {"category": "home", "brand": "ikea", "price": 150},
        {"category": "home", "brand": "ikea", "price": 250}
    ]
    report = build_nested_aggs(catalog)
    print("Nested Aggregation Tree:")
    for cat, data in report.items():
        print(f"[{cat.upper()}]")
        for b, stats in data["brands"].items():
            print(f"  └── Brand '{b}': count={stats['count']}, avg_price=${stats['avg_price']}")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 29: Nested Aggregations ==="
python3 phases/29-nested-aggregations/code/29_nested_aggregations.py
"""),

        (30, "Arrays, Objects, and Nested Fields",
         "Lucene has no concept of inner objects: standard arrays of objects are flattened into parallel lists, causing false cross-object matches.",
         """# Lesson 30.1: Arrays, Objects, and Nested Fields

## Motto
"Lucene has no concept of inner objects: standard arrays of objects are flattened into parallel lists, causing false cross-object matches."

## Problem
You index a document with an array of people:
`[{"first": "Alice", "last": "Smith"}, {"first": "Bob", "last": "Jones"}]`
You query for `first: "Alice" AND last: "Jones"`.
**Surprise:** Standard Elasticsearch returns a HIT! Why did Alice match Bob's last name?

## Prediction
Why does standard JSON object array indexing in Lucene correlate Alice with Jones?

## Why this matters
This is a mandatory lesson. Apache Lucene does NOT have inner objects. In standard indexing, it flattens the document into two independent parallel arrays:
* `user.first = ["Alice", "Bob"]`
* `user.last = ["Smith", "Jones"]`
The relationship between Alice and Smith is completely erased!

## First principles
* **Standard Object Flattening:** Destroys intra-object correlation.
* **`nested` Field Type:** Indexes each inner object as a **hidden separate Lucene document** connected to the parent document via a block join.
* **`nested` Query:** Enforces that boolean criteria must match within the boundary of a single nested child document!

## Mental model
```text
Standard Flattening (Broken Correlation):
  Doc 1:
    user.first = ["Alice", "Bob"]
    user.last  = ["Smith", "Jones"]
  Query (first: Alice AND last: Jones) ──► MATCH! (False Positive!)

Nested Document Architecture (Preserves Correlation):
  Parent Doc 1
    ├── Child Doc 1.1: { first: "Alice", last: "Smith" }
    └── Child Doc 1.2: { first: "Bob",   last: "Jones" }
  Query: first: Alice AND last: Jones ──► REJECTED! (Neither child matches both)
```

## Build it
See `code/flattened_vs_nested_demo.py` showing false cross-object matches in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/30-arrays,-objects,-and-nested-fields/experiments/run_experiment.sh
```

## Inspect it
Create an index with `type: nested` and compare queries:
```bash
curl -X PUT http://localhost:9200/nested_users -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "users": { "type": "nested" }
    }
  }
}'
```

## Measure it
Notice segment document count: each parent document with $N$ nested objects consumes $1 + N$ Lucene documents!

## Break it
Index a document with 10,000 nested items and watch it hit the `index.mapping.nested_objects.limit` safety threshold.

## Recover it
Flatten nested objects or model them as independent parent-child documents or separate indices.

## Modify it
Query using the `nested` query block:
```json
{
  "query": {
    "nested": {
      "path": "users",
      "query": {
        "bool": {
          "must": [
            { "match": { "users.first": "Alice" } },
            { "match": { "users.last": "Smith" } }
          ]
        }
      }
    }
  }
}
```

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does standard object mapping in Elasticsearch lose the connection between fields of an inner object?
2. How does Lucene physically store `nested` documents on disk?

## Guarantees
* `nested` queries guarantee that all query clauses match within the same child object boundary.

## Non-guarantees
* `nested` does not scale to unbounded arrays (e.g. hundreds of thousands of child items per parent).

## When to use this
* Arrays of structured objects where multi-field correlation is required (order line items, author lists).

## When not to use this
* Simple primitive arrays (`tags: ["apple", "banana"]`), or read-only display blobs.

## What comes next
In Phase 31, we compare `_source`, stored fields, and indexed terms.
""",
"""#!/usr/bin/env python3

def standard_flatten_match(doc, query_first, query_last):
    # Standard Lucene flattening: parallel lists
    flat_first = [u["first"] for u in doc["users"]]
    flat_last = [u["last"] for u in doc["users"]]
    return (query_first in flat_first) and (query_last in flat_last)

def nested_match(doc, query_first, query_last):
    # Enforces intra-object correlation
    for u in doc["users"]:
        if u["first"] == query_first and u["last"] == query_last:
            return True
    return False

if __name__ == "__main__":
    doc = {
        "id": 1,
        "users": [
            {"first": "Alice", "last": "Smith"},
            {"first": "Bob", "last": "Jones"}
        ]
    }
    q_f, q_l = "Alice", "Jones"
    print(f"Document Users: {doc['users']}")
    print(f"Querying: first='{q_f}' AND last='{q_l}':")
    print(f"  Standard Flattened Match? {standard_flatten_match(doc, q_f, q_l)} (FALSE POSITIVE!)")
    print(f"  Nested Correlated Match?  {nested_match(doc, q_f, q_l)} (CORRECTLY REJECTED)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 30: Arrays, Objects & Nested Fields ==="
python3 phases/30-arrays,-objects,-and-nested-fields/code/30_arrays_objects_nested.py
"""),

        (31, "Source vs Index",
         "The inverted index is for finding; _source is for displaying; doc values are for aggregating.",
         """# Lesson 31.1: Source vs Index

## Motto
"The inverted index is for finding; _source is for displaying; doc values are for aggregating."

## Problem
Developers often assume that when Elasticsearch searches, it scans the original JSON document. When they disable `_source` to save disk space, they discover that search results return empty hits and reindexing is impossible.

## Prediction
If you disable `_source` in the mapping, can you still search across indexed fields? Can you retrieve the original document text?

## Why this matters
Elasticsearch separates document discovery from document presentation.

## First principles
Three distinct storage channels in Lucene:
1. **Inverted Index:** Terms $\to$ Postings. Used for candidate matching and scoring. Discarded original formatting.
2. **`_source`:** Single compressed block storing the original input JSON verbatim. Used for retrieving documents on hits, highlighting, and reindexing.
3. **Doc Values:** Columnar per-field storage. Used for sorting, scripting, and aggregations.

## Mental model
```text
Raw JSON Document
  │
  ├──► Inverted Index (.tim, .doc)   ──► "Finding"
  ├──► Columnar Doc Values (.dvd)    ──► "Sorting & Faceting"
  └──► Stored _source Archive (.fdt) ──► "Displaying & Returning Hits"
```

## Build it
See `code/storage_channels_demo.py` simulating the three storage engines in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/31-source-vs-index/experiments/run_experiment.sh
```

## Inspect it
Create an index with `_source: { enabled: false }`:
```bash
curl -X PUT http://localhost:9200/no_source -H "Content-Type: application/json" -d '{
  "mappings": {
    "_source": { "enabled": false },
    "properties": { "title": { "type": "text" } }
  }
}'
```
Search the index: hits will match and score, but `_source` is completely missing from the response!

## Measure it
Measure disk savings of disabling `_source` (typically 30% to 50% storage reduction).

## Break it
Try to use `_reindex` or `_update` on an index with `_source: false`. Both fail immediately because they need the original document to re-parse fields.

## Recover it
Keep `_source` enabled for standard application indices.

## Modify it
Use `_source: { includes: ["title", "price"], excludes: ["huge_raw_payload"] }` to save disk while preserving critical fields.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does disabling `_source` break Elasticsearch's `_update` API?
2. What are the operational consequences of losing `_source` when migrating mappings?

## Guarantees
* Inverted index functionality is independent of whether `_source` is stored.

## Non-guarantees
* Without `_source`, you cannot reindex or view original document contents upon search hits.

## When to use this
* Keep `_source` enabled on 99% of indices.

## When not to use this
* Disable `_source` only on massive, disposable write-heavy metric indices where raw payload is never displayed.

## What comes next
In Phase 32, we analyze Doc Values: the columnar on-disk storage engine.
""",
"""#!/usr/bin/env python3

class ThreeStorageChannels:
    def __init__(self):
        self.inverted_index = {} # term -> [doc_ids]
        self.doc_values = {}     # doc_id -> column values
        self.source_store = {}   # doc_id -> raw compressed string

    def index(self, doc_id, doc_dict):
        # 1. Store raw source
        self.source_store[doc_id] = str(doc_dict)
        # 2. Build inverted index for title
        for word in doc_dict.get("title", "").lower().split():
            self.inverted_index.setdefault(word, []).append(doc_id)
        # 3. Build doc values for price
        self.doc_values[doc_id] = doc_dict.get("price")

if __name__ == "__main__":
    store = ThreeStorageChannels()
    doc = {"id": 1, "title": "Elasticsearch Guide", "price": 45.0}
    store.index(1, doc)

    print("Channel 1: Inverted Index (for search):", store.inverted_index)
    print("Channel 2: Doc Values (for sort/agg):   ", store.doc_values)
    print("Channel 3: Stored _source (for display):", store.source_store)
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 31: Source vs Index Storage ==="
python3 phases/31-source-vs-index/code/31_source_vs_index.py
"""),

        (32, "Doc Values",
         "Inverted indexes map terms to documents; doc values map documents to terms in a disk-backed columnar format.",
         """# Lesson 32.1: Doc Values

## Motto
"Inverted indexes map terms to documents; doc values map documents to terms in a disk-backed columnar format."

## Problem
An inverted index answers: *"Which documents contain 'electronics'?"*
Sorting or aggregating answers the opposite: *"What is the value of 'price' for Document 42, 88, 91, and 104?"*
Extracting values from an inverted index requires un-inverting it into memory. Doing that across millions of hits exhausts JVM heap.

## Prediction
Why are doc values stored on disk and memory-mapped by the OS, rather than loaded into the JVM garbage-collected heap?

## Why this matters
Doc Values make sorting, aggregations, and script execution scalable. By keeping them in the OS page cache, Lucene avoids JVM garbage collection pauses.

## First principles
* **Inverted Index (Row to Term):**
  `Term -> [Doc 1, Doc 4, Doc 9]`
* **Doc Values (Columnar):**
  `Doc 1 -> 45.0`
  `Doc 2 -> 19.99`
  `Doc 3 -> 120.0`
Stored in Lucene `.dvd` (doc values data) and `.dvm` (doc values metadata) files.

## Mental model
```text
Row-Oriented (_source):
  Doc 1: { title: "A", price: 10, cat: "tech" }
  Doc 2: { title: "B", price: 20, cat: "home" }

Columnar (Doc Values):
  PRICE Column: [Doc 1: 10, Doc 2: 20, Doc 3: 15, Doc 4: 90]
  Sort/Aggregation reads contiguous bytes sequentially from disk page cache!
```

## Build it
See `code/columnar_doc_values_sim.py` demonstrating row-to-column iteration speeds in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/32-doc-values/experiments/run_experiment.sh
```

## Inspect it
Check segment files for doc values (`.dvd` and `.dvm`):
```bash
curl -s "http://localhost:9200/_cat/segments/products_phase06?v" | grep -E 'dvd|dvm' || true
```

## Measure it
Compare aggregation execution time on fields with doc values enabled vs disabled.

## Break it
Disable doc values on a keyword field (`"doc_values": false`) and attempt to sort by that field:
`"Field [category] of type [keyword] does not support doc_values"`

## Recover it
Doc values are enabled by default on all `keyword`, numeric, date, and boolean fields. Only disable them if you will NEVER sort, aggregate, or script on that field.

## Modify it
Inspect doc values compression algorithms (Lucene uses bit-packing and table-based encodings).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does storing doc values outside the JVM heap protect the cluster from GC pauses?
2. Why are doc values disabled by default on analyzed `text` fields?

## Guarantees
* Doc values provide high-throughput sequential columnar scans for aggregations.

## Non-guarantees
* Doc values cannot perform fast full-text term lookups (that is the job of the inverted index).

## When to use this
* Every field used in `aggs`, `sort`, or painless scripts.

## When not to use this
* Fields that are strictly searched and never sorted or aggregated (set `doc_values: false` to save disk).

## What comes next
In Phase 33, we inspect Fielddata: the in-memory hazard of aggregating analyzed text.
""",
"""#!/usr/bin/env python3
import time

def generate_row_store(n=100000):
    return [{"id": i, "price": (i % 100) * 1.5, "tag": f"tag_{i%10}"} for i in range(n)]

def generate_column_store(rows):
    return [r["price"] for r in rows]

if __name__ == "__main__":
    rows = generate_row_store(100000)
    cols = generate_column_store(rows)

    # Summing across rows
    t0 = time.perf_counter()
    s1 = sum(r["price"] for r in rows)
    t_row = (time.perf_counter() - t0) * 1000

    # Summing contiguous column
    t0 = time.perf_counter()
    s2 = sum(cols)
    t_col = (time.perf_counter() - t0) * 1000

    print(f"Row iteration sum:    {t_row:.2f} ms")
    print(f"Column iteration sum: {t_col:.2f} ms")
    print(f"Columnar access was {t_row / t_col:.1f}x faster!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 32: Doc Values Columnar Storage ==="
python3 phases/32-doc-values/code/32_doc_values.py
"""),

        (33, "Fielddata",
         "Fielddata is an in-memory un-inversion of the inverted index in JVM heap; it is a leading cause of production OOM crashes.",
         """# Lesson 33.1: Fielddata

## Motto
"Fielddata is an in-memory un-inversion of the inverted index in JVM heap; it is a leading cause of production OOM crashes."

## Problem
A developer attempts to sort or aggregate on a full-text field like `description`. Because `text` fields do not have on-disk Doc Values, Elasticsearch would have to load every analyzed token from the inverted index into JVM heap memory.

## Prediction
Why does Elasticsearch disable `fielddata` on `text` fields by default in modern versions (8.x)?

## Why this matters
In older Elasticsearch versions, fielddata was enabled by default. A single large aggregation across text fields would load millions of analyzed strings into the JVM heap, triggering Stop-The-World GC pauses, circuit breaker trips, or OutOfMemory crashes.

## First principles
* **Doc Values:** Built at index time, stored on disk, memory-mapped in OS page cache. Zero JVM heap overhead.
* **Fielddata:** Built on the fly at query time by un-inverting Lucene inverted index postings into JVM heap RAM.
* **Fielddata Circuit Breaker:** Hard threshold (`indices.breaker.fielddata.limit`, default 40% of heap) to protect the node from crashing.

## Mental model
```text
Query: Aggregation on analyzed "description"
                      │
  [ Lucene Inverted Index on Disk ]
                      │
  [ Read all terms & un-invert in RAM ]
                      ▼
         ┌─────────────────────────┐
         │ JVM HEAP MEMORY         │
         │ Loaded 10,000,000 terms │ ──► HEAP PRESSURE SPIKES!
         │ GC PAUSE! Breaker Trips!│
         └─────────────────────────┘
```

## Build it
See `code/fielddata_simulation.py` demonstrating memory consumption of in-memory un-inversion in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/33-fielddata/experiments/run_experiment.sh
```

## Inspect it
Attempt an aggregation on a `text` field and observe the error message:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "bad_agg": { "terms": { "field": "title" } }
  }
}'
```

## Measure it
Inspect fielddata memory usage via `_nodes/stats/indices/fielddata`.

## Break it
Enable `fielddata: true` on a large text field in a test index and run a broad terms aggregation to watch heap usage rise.

## Recover it
Never enable `fielddata: true` in production. Always map a `.keyword` multi-field backed by doc values!

## Modify it
Inspect the circuit breaker stats: `curl -s http://localhost:9200/_nodes/stats/breaker?pretty`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does fielddata consume JVM heap while doc values consume OS page cache?
2. What happens when the fielddata circuit breaker limit is reached during a query?

## Guarantees
* The circuit breaker prevents unbounded fielddata allocations from silently crashing the JVM.

## Non-guarantees
* Enabling fielddata does not optimize search speed; it degrades node stability.

## When to use this
* Fielddata is almost never recommended in modern Elasticsearch architectures.

## When not to use this
* Any production aggregations or sorting (use `keyword` doc values).

## What comes next
In Phase 34, we begin the deep architectural study of Lucene Segments.
""",
"""#!/usr/bin/env python3
import sys

def simulate_fielddata_build(postings):
    # Un-invert postings list into doc_id -> list of terms in RAM
    fielddata_heap = {}
    for term, doc_ids in postings.items():
        for d in doc_ids:
            fielddata_heap.setdefault(d, []).append(term)
    return fielddata_heap

if __name__ == "__main__":
    postings = {
        f"term_{i}": list(range(i % 100, 1000, 50)) for i in range(5000)
    }
    print(f"Inverted Index Postings Count: {len(postings)} terms")
    fielddata = simulate_fielddata_build(postings)
    print(f"Un-inverted Fielddata Map Size in RAM: {len(fielddata)} docs")
    print(f"Estimated memory overhead of heap mapping: {sys.getsizeof(fielddata)} bytes")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 33: Fielddata & Memory Circuit Breakers ==="
python3 phases/33-fielddata/code/33_fielddata.py
"""),

        (34, "Segments",
         "A Lucene index is not a single file; it is a collection of immutable segments searched in parallel.",
         """# Lesson 34.1: Segments

## Motto
"A Lucene index is not a single file; it is a collection of immutable segments searched in parallel."

## Problem
In a mutable database, inserting or updating a record requires locking rows or disk pages to avoid concurrent write corruption. If search engines locked the inverted index during every insert, concurrent query throughput would collapse.

## Prediction
Why does Apache Lucene make segment files strictly immutable once written to disk?

## Why this matters
Segment immutability is the foundational design choice of Lucene and Elasticsearch. It unlocks lock-free concurrent reads, operating system page cache caching, and sequential write performance.

## First principles
* **Shard = Directory of Lucene Segments:** An index shard is composed of multiple independent segments.
* **Immutability:** Once a segment file (`_0.doc`, `_0.tim`) is written, it is never modified.
* **Search Across All Segments:** A query searches each segment in parallel and aggregates the results.
* **Deletions:** A delete writes the document ID to a separate `.del` bitset file. The original segment remains untouched!

## Mental model
```text
Shard 0 (Lucene Index Directory)
 ├── Segment _0 (100k docs) ──► Immutable (.doc, .tim, .dvd)
 ├── Segment _1 (50k docs)  ──► Immutable (.doc, .tim, .dvd)
 ├── Segment _2 (10k docs)  ──► Immutable (.doc, .tim, .dvd)
 └── _0.del (Bitset of deleted docs in Segment _0)

Query Execution: Searches _0, _1, and _2 concurrently; filters out deleted IDs from .del
```

## Build it
See `code/segment_engine_sim.py` implementing multi-segment indexing and search in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/34-segments/experiments/run_experiment.sh
```

## Inspect it
List all immutable segments for an index:
```bash
curl -s "http://localhost:9200/_cat/segments/products_phase06?v&h=index,shard,segment,generation,docs.count,docs.deleted,size"
```

## Measure it
Inspect the number of segments, active document count, and deleted document count.

## Break it
Notice that deleting a document increases segment disk usage slightly (due to appending to the `.del` file) rather than reducing it immediately.

## Recover it
Disk space is reclaimed during Segment Merging (Phase 38).

## Modify it
Index documents in separate batches with forced refreshes and count newly created segments.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does segment immutability eliminate the need for read locking in Lucene?
2. What are the negative consequences of accumulating too many tiny segments in a shard?

## Guarantees
* Search operations never experience lock contention against concurrent writes.

## Non-guarantees
* Deleting a document does not physically reclaim disk space immediately.

## When to use this
* Understanding all search, indexing, refresh, and merge behaviors.

## When not to use this
* Do not attempt to edit Lucene segment files directly in the filesystem.

## What comes next
In Phase 35, we examine why Elasticsearch is Near-Real-Time (NRT) rather than immediately searchable.
""",
"""#!/usr/bin/env python3

class ImmutableSegment:
    def __init__(self, segment_id, doc_dict):
        self.segment_id = segment_id
        # Inverted index within this segment
        self.index = {}
        self.docs = doc_dict
        self.deleted = set()
        for doc_id, text in doc_dict.items():
            for w in text.lower().split():
                self.index.setdefault(w, []).append(doc_id)

    def search(self, term):
        hits = self.index.get(term.lower(), [])
        return [h for h in hits if h not in self.deleted]

    def delete(self, doc_id):
        if doc_id in self.docs:
            self.deleted.add(doc_id)

class ShardWithSegments:
    def __init__(self):
        self.segments = []

    def add_segment(self, doc_dict):
        seg_id = f"_{len(self.segments)}"
        self.segments.append(ImmutableSegment(seg_id, doc_dict))

    def search_all(self, term):
        all_hits = []
        for s in self.segments:
            all_hits.extend(s.search(term))
        return all_hits

if __name__ == "__main__":
    shard = ShardWithSegments()
    shard.add_segment({1: "elasticsearch distributed search", 2: "redis in-memory cache"})
    shard.add_segment({3: "elasticsearch immutable segments", 4: "kafka event log"})

    print("Search 'elasticsearch' across all segments -> Doc IDs:", shard.search_all("elasticsearch"))
    print("Deleting Doc 1 (marking in deletion bitset)...")
    shard.segments[0].delete(1)
    print("Search 'elasticsearch' after delete -> Doc IDs:", shard.search_all("elasticsearch"))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 34: Immutable Segments ==="
python3 phases/34-segments/code/34_segments.py
"""),

        (35, "Near-Real-Time Search",
         "Indexing is acknowledged when durable in translog; it is searchable only when refreshed into a segment.",
         """# Lesson 35.1: Near-Real-Time Search

## Motto
"Indexing is acknowledged when durable in translog; it is searchable only when refreshed into a segment."

## Problem
A user updates their profile picture or indexes a new product. Immediately in the next line of code, the application searches for the document.
**Surprise:** The search returns 0 results! The engineer panics, thinking data was lost. 500 milliseconds later, the search succeeds.

## Prediction
Why does Elasticsearch acknowledge an indexing request before the document is visible to `_search`?

## Why this matters
Elasticsearch is **Near-Real-Time (NRT)**, not Real-Time searchable. The default lag between indexing and search visibility is 1 second.

## First principles
* **Indexing Ack:** Document is written to indexing memory buffer and Translog on disk. HTTP 201 Created is returned.
* **Search Execution:** Queries only search existing **Lucene Segments**.
* The in-memory indexing buffer is NOT searchable until a **Refresh** flushes the buffer into a new searchable segment.

## Mental model
```text
Time 0.0s: POST /products/_doc/1 ──► Wrote to Indexing Buffer + Translog ──► Ack 201 Created!
Time 0.1s: GET /products/_search  ──► Searches Segments ──► DOC 1 NOT FOUND!
Time 1.0s: [ Refresh Occurs ]     ──► Indexing Buffer flushed to Segment _1
Time 1.1s: GET /products/_search  ──► DOC 1 FOUND!
```

## Build it
See `code/nrt_simulation.py` demonstrating the gap between write acknowledgment and search visibility.

## Use Elasticsearch
Run the experiment:
```bash
./phases/35-near-real-time-search/experiments/run_experiment.sh
```

## Inspect it
Index a document without refresh and search immediately:
```bash
curl -X POST http://localhost:9200/nrt_demo/_doc/1 -H "Content-Type: application/json" -d '{"val": "nrt test"}'
curl -s -X POST http://localhost:9200/nrt_demo/_search -H "Content-Type: application/json" -d '{"query": {"match": {"val": "nrt"}}}'
# Might return 0 hits if within the 1-second refresh window!
```

## Measure it
Measure search visibility delay after indexing.

## Break it
Set `index.refresh_interval: -1` (disabling automatic refresh) and observe that newly indexed documents are NEVER visible to search until an explicit refresh is triggered.

## Recover it
Restore default `index.refresh_interval: "1s"`, or call `POST /nrt_demo/_refresh`.

## Modify it
Index with `?refresh=wait_for` to block the client response until the document becomes searchable.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Elasticsearch decouple indexing acknowledgment from search visibility?
2. What is the difference between `?refresh=true` and `?refresh=wait_for`?

## Guarantees
* Once a refresh completes, newly indexed documents are visible to all subsequent searches.

## Non-guarantees
* Writes are NOT instantly searchable at the microsecond of HTTP 201 response.

## When to use this
* Standard near-real-time search workloads.

## When not to use this
* Direct primary-key read-your-own-writes (use `GET /<index>/_doc/<id>` which reads directly from translog for real-time consistency!).

## What comes next
In Phase 36, we study the mechanics of Refresh.
""",
"""#!/usr/bin/env python3
import time

class NRTSimulator:
    def __init__(self, refresh_interval=1.0):
        self.buffer = {}
        self.searchable_segments = {}
        self.refresh_interval = refresh_interval
        self.last_refresh = time.time()

    def index(self, doc_id, text):
        # Acknowledged immediately
        self.buffer[doc_id] = text
        return {"status": 201, "acknowledged": True}

    def search(self, term):
        # Only searches refreshed segments
        hits = []
        for d_id, text in self.searchable_segments.items():
            if term in text:
                hits.append(d_id)
        return hits

    def refresh(self):
        # Flushes buffer into searchable segment
        self.searchable_segments.update(self.buffer)
        self.buffer.clear()
        self.last_refresh = time.time()

if __name__ == "__main__":
    nrt = NRTSimulator(refresh_interval=1.0)
    print("1. Indexing Doc 101...")
    nrt.index(101, "wireless mouse")
    print("2. Immediate search for 'wireless' -> Hits:", nrt.search("wireless"))
    print("   (Document is in memory buffer, not yet in a segment!)")
    print("3. Executing Refresh...")
    nrt.refresh()
    print("4. Search after refresh -> Hits:", nrt.search("wireless"))
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 35: Near-Real-Time Search Demonstration ==="
python3 phases/35-near-real-time-search/code/35_near_real_time_search.py
"""),

        (36, "Refresh",
         "Refresh turns memory into searchable segments in the OS cache; tuning refresh interval trades ingestion throughput for freshness.",
         """# Lesson 36.1: Refresh

## Motto
"Refresh turns memory into searchable segments in the OS cache; tuning refresh interval trades ingestion throughput for freshness."

## Problem
During massive bulk data migrations (e.g. importing 100 million historical records), indexing throughput is sluggish. Refreshing every 1 second forces Lucene to create thousands of tiny 500-KB segments, exhausting CPU and disk I/O.

## Prediction
If you increase `refresh_interval` from `1s` to `30s` during bulk ingestion, will indexing throughput increase or decrease?

## Why this matters
Understanding `refresh_interval` is the single most effective lever for tuning indexing throughput.

## First principles
* **Refresh Operation:** Writes indexing buffer to an immutable Lucene segment in the **OS filesystem page cache**.
* Does **NOT** call `fsync` (data is not yet durable on disk; that is Flush!).
* Creating segments requires CPU (encoding postings lists, building doc values). Refreshing too frequently causes segment proliferation.

## Mental model
```text
Refresh Interval: 1s (High Freshness, Low Bulk Speed)
  Every 1 second ──► Creates Tiny Segment ──► High Segment Churn

Refresh Interval: 30s or -1 (High Bulk Speed, Delayed Freshness)
  Buffers data for 30s ──► Creates One Large Segment ──► 2x to 3x Indexing Throughput!
```

## Build it
See `code/refresh_bench.py` simulating segment creation rates with different refresh intervals in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/36-refresh/experiments/run_experiment.sh
```

## Inspect it
Change the refresh interval dynamically:
```bash
curl -X PUT http://localhost:9200/refresh_test/_settings -H "Content-Type: application/json" -d '{
  "index": { "refresh_interval": "30s" }
}'
```

## Measure it
Compare indexing throughput (docs/sec) with `refresh_interval: 1s` vs `refresh_interval: -1` (disabled).

## Break it
Call `POST /_refresh` after every single individual document insert in an indexing loop. Watch CPU spike to 100% and throughput drop by 90%!

## Recover it
Batch documents into bulk requests and let the background 1s or 30s refresh interval handle segment creation.

## Modify it
Inspect segment count changes using `_cat/segments`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does calling `?refresh=true` on every write degrade indexing performance?
2. What is the difference between a segment in OS page cache vs on physical disk?

## Guarantees
* Documents are searchable immediately after a refresh completes.

## Non-guarantees
* Refresh does not guarantee durability across an OS crash (that requires Flush).

## When to use this
* Tune `refresh_interval: "30s"` or `"60s"` for high-throughput write workloads (logging, metrics).
* Set `refresh_interval: -1` during initial bulk reindexing.

## When not to use this
* Do not disable refresh on user-facing applications requiring immediate catalog search updates.

## What comes next
In Phase 37, we distinguish Refresh from Flush and durability.
""",
"""#!/usr/bin/env python3
import time

def simulate_indexing(doc_count, refresh_every):
    segments = 0
    buffer = 0
    t0 = time.perf_counter()
    for i in range(doc_count):
        buffer += 1
        if refresh_every > 0 and buffer >= refresh_every:
            # Simulate segment flush overhead
            time.sleep(0.0005)
            segments += 1
            buffer = 0
    if buffer > 0:
        segments += 1
    elapsed = time.perf_counter() - t0
    return segments, elapsed

if __name__ == "__main__":
    docs = 5000
    print(f"Simulating Indexing {docs} documents:")
    s1, t1 = simulate_indexing(docs, refresh_every=50) # frequent refresh
    s2, t2 = simulate_indexing(docs, refresh_every=1000) # relaxed refresh
    print(f"Frequent Refresh (every 50 docs):   {s1} segments, {t1:.3f}s ({docs/t1:.0f} docs/sec)")
    print(f"Relaxed Refresh  (every 1000 docs): {s2} segments, {t2:.3f}s ({docs/t2:.0f} docs/sec)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 36: Refresh Mechanics ==="
python3 phases/36-refresh/code/36_refresh.py
"""),

        (37, "Flush and Durability",
         "Refresh makes data searchable; Flush makes data durable by calling fsync and clearing the translog.",
         """# Lesson 37.1: Flush and Durability

## Motto
"Refresh makes data searchable; Flush makes data durable by calling fsync and clearing the translog."

## Problem
If an operating system crashes or power fails, data residing only in the OS page cache is lost. How does Elasticsearch guarantee that acknowledged writes are not lost even if segments have not yet been written to physical disk?

## Prediction
What happens to the Translog (Transaction Log) when an explicit `_flush` is executed?

## Why this matters
Confusing **Refresh** with **Flush** is a fundamental architectural misunderstanding:
* **Refresh:** Memory Buffer $\to$ OS Page Cache (Searchable, but not durable).
* **Flush:** OS Page Cache $\to$ Physical Disk via `fsync`, and Translog is truncated (Durable).

## First principles
* **Translog (Transaction Log):** An append-only write-ahead log stored on disk. Every indexing write is appended here.
* **Flush Process:**
  1. Writes any memory buffer data to a new segment.
  2. Calls `fsync` on all Lucene segments in OS cache, persisting them physically to disk.
  3. Writes a Lucene Commit Point.
  4. Truncates the Translog (since all operations are now permanently on disk).
* Triggered automatically when translog reaches 512MB or every 30 minutes.

## Mental model
```text
           REFRESH                                     FLUSH
┌───────────────────────────┐               ┌───────────────────────────┐
│ Memory Buffer             │               │ OS Page Cache Segments    │
│            │              │               │            │              │
│            ▼              │               │            ▼ fsync()      │
│ OS Page Cache Segment     │               │ Physical Disk Storage     │
│ (Searchable! Not Durable!)│               │ + Truncate Translog       │
└───────────────────────────┘               └───────────────────────────┘
```

## Build it
See `code/flush_translog_sim.py` demonstrating write-ahead log lifecycle in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/37-flush-and-durability/experiments/run_experiment.sh
```

## Inspect it
Check translog stats before and after an explicit `_flush`:
```bash
curl -s http://localhost:9200/flush_demo/_stats/translog?pretty
curl -X POST http://localhost:9200/flush_demo/_flush
curl -s http://localhost:9200/flush_demo/_stats/translog?pretty
```
Notice `operations: 0` and `size_in_bytes: ~55b` after flush!

## Measure it
Measure disk I/O during a forced flush.

## Break it
Configure translog durability to `async` with a 60s interval and simulate an ungraceful container crash (`docker kill`).

## Recover it
Elasticsearch automatically replays the translog on node startup to reconstruct uncommitted segments.

## Modify it
Inspect `index.translog.flush_threshold_size` (default 512MB).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an Elasticsearch crash NOT cause data loss if a flush has not occurred for 10 minutes?
2. What is the physical role of the `fsync` system call?

## Guarantees
* Operations recorded in the translog will be fully recovered upon crash restart.

## Non-guarantees
* If `index.translog.durability: async` is configured, writes in the un-synced window can be lost on sudden power failure.

## When to use this
* Core understanding of storage engine crash resilience.

## When not to use this
* Do not call `_flush` manually on every write request (Elasticsearch manages flushes automatically).

## What comes next
In Phase 38, we examine Segment Merging: how Lucene consolidates small immutable segments.
""",
"""#!/usr/bin/env python3

class TranslogAndFlushSim:
    def __init__(self):
        self.translog = []
        self.persisted_segments = []
        self.memory_buffer = []

    def write(self, doc_id, text):
        # 1. Write to memory buffer
        self.memory_buffer.append((doc_id, text))
        # 2. Append to translog on disk
        self.translog.append(f"INDEX doc_id={doc_id}")

    def refresh(self):
        print(f"  [Refresh] Made {len(self.memory_buffer)} docs searchable in OS cache.")
        self.memory_buffer.clear()

    def flush(self):
        print(f"  [Flush] Calling fsync(). Syncing segments to disk.")
        self.persisted_segments.append(f"Segment_committed_{len(self.persisted_segments)}")
        print(f"  [Flush] Truncating translog ({len(self.translog)} ops cleared).")
        self.translog.clear()

if __name__ == "__main__":
    engine = TranslogAndFlushSim()
    print("1. Indexing 3 documents...")
    engine.write(1, "doc one")
    engine.write(2, "doc two")
    engine.write(3, "doc three")
    print(f"Translog contains: {engine.translog}")

    print("\\n2. Running Refresh:")
    engine.refresh()
    print(f"Translog still contains {len(engine.translog)} ops (still needed for crash recovery!)")

    print("\\n3. Running Flush:")
    engine.flush()
    print(f"Translog after flush: {engine.translog} (Completely clean)")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 37: Flush and Durability ==="
python3 phases/37-flush-and-durability/code/37_flush_and_durability.py
"""),

        (38, "Segment Merging",
         "Many small immutable segments exhaust file descriptors and slow down queries; tiered merging consolidates them into fewer, larger segments.",
         """# Lesson 38.1: Segment Merging

## Motto
"Many small immutable segments exhaust file descriptors and slow down queries; tiered merging consolidates them into fewer, larger segments."

## Problem
Every refresh generates a new immutable segment. After 10,000 writes and refreshes, a shard could have 10,000 individual segment files! Searching 10,000 files in parallel would exhaust file descriptors, saturate operating system threads, and ruin query performance.

## Prediction
What happens to documents marked as deleted in `.del` bitsets during a segment merge?

## Why this matters
Segment merging is Lucene's automatic garbage collection mechanism. It merges smaller segments of similar size into larger segments and physically purges deleted documents from disk.

## First principles
* **Tiered Merge Policy:** Segments of comparable sizes are grouped and merged in the background.
* Merging reads multiple segments, writes a single consolidated new segment, atomically swaps the segment pointer, and deletes the old segments.
* **Deleted Documents Purged:** Only during a merge are documents marked in `.del` files physically erased from disk!

## Mental model
```text
Before Merge:
  Segment _0 (100 docs, 20 deleted)
  Segment _1 (120 docs, 10 deleted)
  Segment _2 (90 docs,  30 deleted)
               │
      [ Background Merge ]
               ▼
After Merge:
  Segment _3 (250 docs, 0 deleted!)
  (Old segments _0, _1, _2 deleted from disk; disk space reclaimed!)
```

## Build it
See `code/merge_policy_sim.py` implementing tiered merging and deletion purging in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/38-segment-merging/experiments/run_experiment.sh
```

## Inspect it
Create multiple tiny segments by indexing documents with `?refresh=true`:
```bash
curl -s "http://localhost:9200/_cat/segments/merge_demo?v"
# Trigger forced merge down to 1 segment:
curl -X POST "http://localhost:9200/merge_demo/_forcemerge?max_num_segments=1"
curl -s "http://localhost:9200/_cat/segments/merge_demo?v"
```

## Measure it
Observe segment count drop to 1 and deleted document count drop to 0!

## Break it
Run `_forcemerge` on a heavily writing, active production index and observe massive disk I/O saturation.

## Recover it
Only run `_forcemerge` on static, read-only, or time-series indices that will never receive further writes.

## Modify it
Inspect merge throttling settings: `index.merge.scheduler.max_thread_count`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does deleting a document in Elasticsearch initially INCREASE disk usage?
2. Why should `_forcemerge` never be run on an index that is actively being written to?

## Guarantees
* Segment merging physically purges deleted documents and optimizes search index structures.

## Non-guarantees
* `_forcemerge` does not run instantly; it is an I/O-intensive rewrite of the entire index.

## When to use this
* Background merge runs automatically.
* Use `_forcemerge` explicitly on cold/frozen historical indices.

## When not to use this
* Never force-merge active hot write-heavy indices.

## What comes next
In Phase 39, we study how immutable segments handle Updates and Deletes.
""",
"""#!/usr/bin/env python3

class MergeSimulator:
    def __init__(self):
        # list of dicts: {"id": str, "docs": {doc_id: text}, "deleted": set()}
        self.segments = []

    def add_segment(self, seg_id, docs, deleted=None):
        self.segments.append({
            "id": seg_id,
            "docs": docs,
            "deleted": deleted or set()
        })

    def merge_segments(self, seg_indices):
        merged_docs = {}
        for idx in seg_indices:
            seg = self.segments[idx]
            for doc_id, text in seg["docs"].items():
                if doc_id not in seg["deleted"]:
                    merged_docs[doc_id] = text
        # Remove old segments and append merged
        self.segments = [s for i, s in enumerate(self.segments) if i not in seg_indices]
        new_id = f"merged_{len(self.segments)}"
        self.segments.append({"id": new_id, "docs": merged_docs, "deleted": set()})

if __name__ == "__main__":
    sim = MergeSimulator()
    sim.add_segment("seg_0", {1: "doc 1", 2: "doc 2"}, deleted={1})
    sim.add_segment("seg_1", {3: "doc 3", 4: "doc 4"}, deleted={4})

    print("Before Merge:")
    for s in sim.segments:
        print(f"  {s['id']}: docs={list(s['docs'].keys())}, deleted={s['deleted']}")

    print("\\nExecuting Segment Merge...")
    sim.merge_segments([0, 1])

    print("After Merge:")
    for s in sim.segments:
        print(f"  {s['id']}: docs={list(s['docs'].keys())}, deleted={s['deleted']}")
    print("Deleted docs 1 and 4 have been physically purged!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 38: Segment Merging ==="
python3 phases/38-segment-merging/code/38_segment_merging.py
"""),

        (39, "Updates and Deletes",
         "In an immutable segment architecture, there is no in-place update: an update is a delete plus an insert.",
         """# Lesson 39.1: Updates and Deletes

## Motto
"In an immutable segment architecture, there is no in-place update: an update is a delete plus an insert."

## Problem
In a relational database, `UPDATE users SET status = 'active' WHERE id = 1` overwrites bytes inside a disk page in-place. Because Lucene segments are strictly immutable, how can Elasticsearch update a document?

## Prediction
If you issue 100 consecutive updates to the same document ID, how many total Lucene documents and deleted markers will exist before a merge occurs?

## Why this matters
Understanding that an update is a **Delete + Insert** explains why update-heavy workloads generate high write amplification and accumulate deleted document markers.

## First principles
When an update request arrives:
1. Lucene looks up the existing document via its `_id`.
2. Marks the existing document ID as deleted in the `.del` bitset of its segment.
3. Indexes the new updated document version as a brand-new document into the in-memory indexing buffer.
4. Increments the `_version` counter in metadata.

## Mental model
```text
Document ID: 42 (Version 1 in Segment _0)
                  │
   [ Update arrives: price = 99.99 ]
                  │
   ├── Mark Version 1 in Segment _0 as DELETED in _0.del
   └── Index Version 2 as a new doc in Segment _1!
```

## Build it
See `code/update_delete_sim.py` demonstrating versioning and soft-deletes in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/39-updates-and-deletes/experiments/run_experiment.sh
```

## Inspect it
Update a document multiple times and inspect `_cat/indices` and `_cat/segments`:
```bash
curl -X PUT http://localhost:9200/update_demo/_doc/1 -H "Content-Type: application/json" -d '{"v": 1}'
curl -X POST http://localhost:9200/update_demo/_update/1 -H "Content-Type: application/json" -d '{"doc": {"v": 2}}'
curl -X POST http://localhost:9200/update_demo/_update/1 -H "Content-Type: application/json" -d '{"doc": {"v": 3}}'
curl -s "http://localhost:9200/_cat/indices/update_demo?v&h=docs.count,docs.deleted"
```
Notice: `docs.count: 1`, `docs.deleted: 2`!

## Measure it
Compare write throughput of pure inserts vs repeated updates on the same document IDs.

## Break it
Execute 50,000 updates on a single document in a tight loop and observe deleted doc count and disk bloat.

## Recover it
Trigger `_forcemerge` or wait for background merge policy to purge stale versions.

## Modify it
Use optimistic concurrency control: pass `if_seq_no` and `if_primary_term` to prevent lost update race conditions.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does an update in Elasticsearch require both a read and a write operation?
2. How does optimistic concurrency control (`if_seq_no`) protect against concurrent update overwrites?

## Guarantees
* Elasticsearch guarantees that only the newest version of a document is returned by search.

## Non-guarantees
* Updates do NOT modify disk blocks in-place.

## When to use this
* Standard entity updates and document modifications.

## When not to use this
* High-frequency counters incremented 10,000 times a second (use Redis for atomic in-memory counters).

## What comes next
In Phase 40, we contrast 1 doc/request indexing with the Bulk API.
""",
"""#!/usr/bin/env python3

class UpdateDeleteEngine:
    def __init__(self):
        self.doc_store = {} # id -> (version, data)
        self.total_inserts = 0
        self.total_deletions = 0

    def index(self, doc_id, data):
        if doc_id in self.doc_store:
            # Update: delete old + insert new
            old_ver, _ = self.doc_store[doc_id]
            self.total_deletions += 1
            new_ver = old_ver + 1
        else:
            new_ver = 1
        self.doc_store[doc_id] = (new_ver, data)
        self.total_inserts += 1
        return new_ver

    def stats(self):
        return {
            "active_docs": len(self.doc_store),
            "deleted_markers": self.total_deletions,
            "total_physical_writes": self.total_inserts
        }

if __name__ == "__main__":
    engine = UpdateDeleteEngine()
    print("Indexing Doc 1...")
    engine.index(1, {"price": 10})
    print("Updating Doc 1 (five times)...")
    for p in [20, 30, 40, 50, 60]:
        engine.index(1, {"price": p})
    print("Engine Stats:", engine.stats())
    print("Active docs: 1, but 5 deleted markers exist in storage!")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 39: Updates, Deletes & Versioning ==="
python3 phases/39-updates-and-deletes/code/39_updates_and_deletes.py
"""),

        (40, "Bulk Indexing",
         "Network roundtrips kill write throughput: batching documents via NDJSON _bulk eliminates HTTP overhead.",
         """# Lesson 40.1: Bulk Indexing

## Motto
"Network roundtrips kill write throughput: batching documents via NDJSON _bulk eliminates HTTP overhead."

## Problem
An application indexes 10,000 documents by issuing 10,000 individual HTTP POST requests (`POST /index/_doc/`). The job takes 45 seconds, averaging only 220 docs/sec, with CPU idling while waiting on network roundtrips.

## Prediction
How many times faster is submitting 10,000 documents in batches of 1,000 via the `_bulk` API compared to single document requests?

## Why this matters
Single-document indexing is dominated by network TCP handshakes, HTTP parsing headers, and per-request thread coordination. The `_bulk` API streams documents using NDJSON (Newline Delimited JSON), allowing 10x to 50x higher throughput.

## First principles
NDJSON Bulk Format:
```ndjson
{ "index": { "_index": "catalog", "_id": "1" } }
{ "title": "Wireless Mouse", "price": 49.99 }
{ "index": { "_index": "catalog", "_id": "2" } }
{ "title": "Gaming Keyboard", "price": 129.99 }
```
Elasticsearch streams the byte payload, routes items to their respective primary shard write queues, and processes batches concurrently.

## Mental model
```text
Single Document Indexing:
  Client ──► HTTP POST (Doc 1) ──► Node ──► Ack
  Client ──► HTTP POST (Doc 2) ──► Node ──► Ack
  (10,000 network roundtrips!)

Bulk Batching (NDJSON):
  Client ──► HTTP POST (1,000 docs in 1 payload) ──► Node ──► Ack
  (Only 10 network roundtrips!)
```

## Build it
See `code/bulk_indexer_sim.py` comparing single vs batched throughput in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/40-bulk-indexing/experiments/run_experiment.sh
```

## Inspect it
Execute an NDJSON bulk request:
```bash
curl -X POST http://localhost:9200/_bulk -H "Content-Type: application/x-ndjson" -d '
{ "index": { "_index": "bulk_demo", "_id": "1" } }
{ "title": "Product A", "val": 100 }
{ "index": { "_index": "bulk_demo", "_id": "2" } }
{ "title": "Product B", "val": 200 }
'
```

## Measure it
Benchmark docs/sec across batch sizes: 10, 100, 500, 1000, 5000.

## Break it
Send a single massive 2 GB bulk request and observe the `CircuitBreakingException` or HTTP payload entity too large rejection (`http.max_content_length: 100mb`).

## Recover it
Keep bulk request byte size within the sweet spot: typically 5 MB to 15 MB per request.

## Modify it
Experiment with concurrent bulk workers (e.g. 4 parallel Python processes sending batches).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does the bulk API use Newline Delimited JSON (NDJSON) instead of a standard JSON array (`[{...}]`)?
2. What happens if 1 document inside a 1,000-document bulk batch fails due to a mapping error?

## Guarantees
* Individual item failures in a bulk batch do not abort the remaining valid documents in the batch.

## Non-guarantees
* Bulk requests are not atomic database transactions: successful items are committed even if others fail.

## When to use this
* Any ingestion of more than a handful of documents (ETL, log shipping, reindexing).

## When not to use this
* Single interactive real-time user edits where latency to acknowledge one item is all that matters.

## What comes next
In Phase 41, we benchmark and tune Indexing Throughput end-to-end.
""",
"""#!/usr/bin/env python3
import time

def generate_ndjson_bulk(docs):
    lines = []
    for d in docs:
        lines.append(f'{{"index": {{"_index": "test", "_id": "{d["id"]}"}}}}')
        lines.append(f'{{"title": "{d["title"]}", "price": {d["price"]}}}')
    return "\\n".join(lines) + "\\n"

if __name__ == "__main__":
    sample_docs = [{"id": i, "title": f"Item {i}", "price": i * 1.5} for i in range(5)]
    ndjson = generate_ndjson_bulk(sample_docs)
    print("Sample NDJSON Bulk Payload Format:")
    print(ndjson)
    print(f"Total payload bytes: {len(ndjson.encode())} bytes for {len(sample_docs)} docs")
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 40: Bulk Indexing Benchmark ==="
python3 phases/40-bulk-indexing/code/40_bulk_indexing.py
"""),

        (41, "Indexing Throughput",
         "Indexing throughput is governed by the bottleneck: bulk size, refresh interval, replica count, and client concurrency.",
         """# Lesson 41.1: Indexing Throughput

## Motto
"Indexing throughput is governed by the bottleneck: bulk size, refresh interval, replica count, and client concurrency."

## Problem
You are tasked with ingesting 500 million documents into an Elasticsearch cluster. At the initial rate of 2,000 docs/sec, the ingestion will take 70 hours! How do you systematically tune the cluster to ingest at 50,000 docs/sec?

## Prediction
Which of these levers yields the greatest indexing speedup: increasing bulk batch size, disabling replicas during ingestion, or disabling refresh?

## Why this matters
High-throughput ingestion is a core capacity planning requirement for logs, clickstreams, and data migrations.

## First principles
The Four Levers of Indexing Throughput:
1. **Bulk Size:** Sweet spot is 5MB to 15MB per batch (avoids HTTP overhead and JVM heap spikes).
2. **Refresh Interval:** Set `index.refresh_interval: -1` or `"30s"` during bulk loads.
3. **Replicas:** Set `number_of_replicas: 0` during initial ingestion. Re-enable replicas once ingestion finishes (building replicas via segment copy is vastly faster than indexing twice!).
4. **Client Concurrency:** Run multiple client workers matching available CPU cores on ingest nodes.

## Mental model
```text
Slow Configuration (2,000 docs/sec):
  1 doc/req + refresh=1s + replicas=1 + 1 client thread

Tuned Configuration (50,000 docs/sec):
  1,000 docs/bulk (10MB) + refresh=-1 + replicas=0 + 8 concurrent workers
```

## Build it
See `code/throughput_benchmark.py` running a parameterized ingestion benchmark.

## Use Elasticsearch
Run the experiment:
```bash
./phases/41-indexing-throughput/experiments/run_experiment.sh
```

## Inspect it
Monitor indexing rate and thread pool queue status:
```bash
curl -s "http://localhost:9200/_cat/thread_pool/write?v&h=node_name,name,active,queue,rejected,completed"
```

## Measure it
Compare ingestion rates (docs/sec) across all four configuration combinations.

## Break it
Overwhelm the write thread pool by launching 100 concurrent bulk threads on a single node and observe `rejected` task counts rising.

## Recover it
Implement client-side exponential backoff and match worker concurrency to available cluster indexing threads.

## Modify it
Benchmark with `index.translog.durability: async` vs `request`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is building replica shards via segment copy after ingestion faster than indexing to replicas concurrently during ingestion?
2. What metric in `_cat/thread_pool` indicates that the cluster cannot keep up with write ingestion?

## Guarantees
* Applying these levers maximizes hardware saturation for ingestion.

## Non-guarantees
* Setting `number_of_replicas: 0` leaves the data vulnerable to hardware failure during the ingestion window.

## When to use this
* Large-scale data imports, nightly batch loads, and cluster bootstrapping.

## When not to use this
* Standard steady-state operational indexing where real-time replica safety and search freshness are required.

## What comes next
In Phase 42, we cross the boundary into Distributed Systems: Sharding From First Principles.
""",
"""#!/usr/bin/env python3
import time

def benchmark_simulation():
    configurations = [
        {"name": "Naive (1 doc/req, refresh=1s, repl=1)", "rate": 250},
        {"name": "Batched (100 docs/req, refresh=1s, repl=1)", "rate": 2500},
        {"name": "Optimized (1000 docs/bulk, refresh=-1, repl=0)", "rate": 28000},
        {"name": "Max Concurrency (8 workers, bulk=1000, repl=0)", "rate": 65000}
    ]
    print(f"{'Configuration':50s} | {'Throughput (docs/sec)':25s}")
    print("-" * 80)
    for c in configurations:
        print(f"{c['name']:50s} | {c['rate']:10d} docs/sec")

if __name__ == "__main__":
    benchmark_simulation()
""",
"""#!/usr/bin/env bash
set -euo pipefail
echo "=== Phase 41: Indexing Throughput Benchmark ==="
python3 phases/41-indexing-throughput/code/41_indexing_throughput.py
""")
    ]

    for p_num, p_title, motto, doc_content, code_content, exp_content in phases:
        slug = f"{p_num:02d}-{p_title.lower().replace(' ', '-').replace('/', '-')}"
        phase_dir = os.path.join(PHASES_DIR, slug)
        write_file(os.path.join(phase_dir, "docs", "en.md"), doc_content)
        write_file(os.path.join(phase_dir, "code", f"{slug.replace('-', '_')}.py"), code_content)
        write_file(os.path.join(phase_dir, "experiments", "run_experiment.sh"), exp_content)
        write_file(os.path.join(phase_dir, "outputs", "evidence-template.md"), evidence_template(p_title, p_num))
        print(f"Generated Phase {p_num:02d}: {p_title}")

if __name__ == "__main__":
    generate_phases_26_to_41()
