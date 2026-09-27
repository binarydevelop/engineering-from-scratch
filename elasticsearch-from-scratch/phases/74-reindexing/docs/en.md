# Lesson 74.1: Reindexing

## Motto
"Lucene mappings are immutable on disk: changing an analyzer or field type requires reindexing to a new index."

## Problem
You indexed 10 million products with `price` as `keyword`. You need to run numeric range queries (`price BETWEEN 50 AND 100`). You try to change the mapping with `PUT /products/_mapping`:
**Elasticsearch Error:** `"Cannot change existing field type from keyword to double"`.

## Prediction
Why can existing field types in a Lucene index NEVER be altered in-place?

## Why this matters
Lucene inverted indexes, BKD trees, and doc values are permanently encoded on disk at write time. To change how a field is indexed, you must create a new index with the correct mapping and copy data over using the `_reindex` API.

## First principles
The Reindex Lifecycle:
1. Create new index `products_v2` with updated settings, analyzers, and mappings.
2. Call `POST /_reindex` to copy documents from `products_v1` to `products_v2`.
3. Elasticsearch reads `_source` from the old index and streams writes through the new mapping pipeline.
4. Verify document counts.
5. Delete old index `products_v1`.

## Mental model
```text
Old Index (products_v1): price is KEYWORD
                 │
      [ POST /_reindex ]
   (Reads _source from v1, parses through new mapping in v2)
                 │
                 ▼
New Index (products_v2): price is DOUBLE (BKD Tree Range Optimized!)
```

## Build it
See `code/reindex_migration_sim.py` demonstrating schema transformation during data migration in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/74-reindexing/experiments/run_experiment.sh
```

## Inspect it
Create `products_v2` and trigger reindex:
```bash
curl -X PUT http://localhost:9200/products_v2 -H "Content-Type: application/json" -d '{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "price": { "type": "double" }
    }
  }
}'
curl -X POST "http://localhost:9200/_reindex?wait_for_completion=true" -H "Content-Type: application/json" -d '{
  "source": { "index": "products_phase06" },
  "dest": { "index": "products_v2" }
}'
```

## Measure it
Inspect reindex progress and throughput via `_tasks?detailed=true&actions=*reindex*`.

## Break it
Attempt to reindex an index that had `_source: false` disabled.
**Observed Failure:** Reindex fails because `_source` is required to re-parse fields!

## Recover it
Always keep `_source: true` enabled.

## Modify it
Use a painless script inside reindex to mutate or rename fields on the fly:
`"script": { "source": "ctx._source.price = ctx._source.price * 1.1" }`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does reindexing require `_source` to be enabled on the source index?
2. How can you throttle `_reindex` so it does not overwhelm cluster write queues? (`requests_per_second`)

## Guarantees
* Reindexing guarantees that data is re-analyzed according to the new index mapping schema.

## Non-guarantees
* Reindexing is not instantaneous; it is an $O(N)$ bulk write operation.

## When to use this
* Changing field types, changing tokenizers/analyzers, altering shard counts.

## When not to use this
* Adding a brand-new field to an existing mapping (new fields can be added dynamically with `PUT /<index>/_mapping` without reindexing!).

## What comes next
In Phase 75, we eliminate downtime during reindexing using Index Aliases.
