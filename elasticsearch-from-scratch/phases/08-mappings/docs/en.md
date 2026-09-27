# Lesson 08.1: Mappings

## Motto
"Dynamic mapping is convenient in development and fatal in production; explicit schema is engineering discipline."

## Problem
If you index `{"order_id": "00123"}` into an unmapped index, Elasticsearch dynamically infers `long` (number `123`), permanently stripping the leading zeros. When the next document arrives with `{"order_id": "00123-A"}`, indexing fails with a mapping conflict!

## Prediction
What happens when you index a document with dynamic mapping disabled (`dynamic: strict`) containing an undocumented field?

## Why this matters
An Elasticsearch mapping defines the type and indexing rules for every field in an index. Once a field mapping is created in Lucene, it can never be altered or deleted without creating a new index and reindexing all data.

## First principles
Dynamic mapping rules:
* `"2026-01-01"` -> inferred as `date`
* `true` / `false` -> inferred as `boolean`
* `123` -> inferred as `long`
* `"hello"` -> inferred as `text` with `.keyword` multi-field

## Mental model
```text
Dynamic Mapping:
  "0042" ──► Auto-detected as LONG ──► Leading zeros destroyed!

Explicit Mapping:
  "order_id": { "type": "keyword" } ──► Stored as exact string "0042"
```

## Build it
See `code/mapping_simulation.py` illustrating dynamic inference edge cases.

## Use Elasticsearch
Run the experiment:
```bash
./phases/08-mappings/experiments/run_experiment.sh
```

## Inspect it
Retrieve the active mapping of an index:
```bash
curl -s http://localhost:9200/strict_products/_mapping?pretty
```

## Measure it
Compare indexing time: dynamic mapping incurs cluster-state update overhead on new fields, whereas explicit mapping indexes immediately without master node coordination.

## Break it
Configure an index with `"dynamic": "strict"` and index a document containing an unmapped field. Observe the `strict_dynamic_mapping_exception`.

## Recover it
Add the field explicitly to the mapping via `PUT /<index>/_mapping` before indexing.

## Modify it
Set `"dynamic": "runtime"` to evaluate fields dynamically at query time without indexing them.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why can existing field types in a mapping never be modified in-place?
2. What is the operational risk of running a production cluster with `dynamic: true`?

## Guarantees
* Explicit mappings strictly enforce data types across all primary and replica shards.

## Non-guarantees
* Elasticsearch does not enforce relational null-checks or cross-field validation.

## When to use this
* Every production index must define an explicit mapping schema.

## When not to use this
* Dynamic mapping should only be used in rapid local prototyping or log collection with unknown formats.

## What comes next
In Phase 09, we trace the full architectural path of an indexing request from HTTP client to disk.
