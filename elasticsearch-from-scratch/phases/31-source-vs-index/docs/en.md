# Lesson 31.1: Source vs Index

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
1. **Inverted Index:** Terms $	o$ Postings. Used for candidate matching and scoring. Discarded original formatting.
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
