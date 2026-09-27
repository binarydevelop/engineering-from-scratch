# Lesson 45.1: Query Then Fetch

## Motto
"Query-Then-Fetch avoids transferring gigabytes of document bodies across nodes during ranking."

## Problem
If an index has 10 shards and you search for `size: 10`, what if each shard returned the full 500-KB `_source` JSON document for its top 10 candidates? 100 full documents (50 MB) would travel across the internal cluster network, only for the coordinator to discard 90 of them!

## Prediction
Why does Elasticsearch execute search in two separate roundtrips (Query phase, then Fetch phase) rather than one combined request?

## Why this matters
**Query-Then-Fetch** is the default search execution type in Elasticsearch. It separates relevance scoring from document retrieval.

## First principles
* **Phase 1 (Query Phase):**
  * Coordinator broadcasts query to all shards.
  * Shards return ONLY `(doc_id, score, sort_values)`.
  * Tiny network payload: a few bytes per candidate!
* **Merge:** Coordinator sorts candidate scores to identify the exact $K$ winning documents.
* **Phase 2 (Fetch Phase):**
  * Coordinator contacts only the specific shards hosting the winning $K$ documents.
  * Requests the full `_source`, stored fields, and highlights for those exact IDs.

## Mental model
```text
Roundtrip 1 (Query Phase):
  Coordinator ──► Shards: "Give me your top 10 IDs and BM25 scores."
  Shards ──────► Coordinator: Returns lightweight ID list: [(42, 3.8), (91, 2.9)...]

Roundtrip 2 (Fetch Phase):
  Coordinator ──► Shard 2: "Give me the full _source for Doc 42."
  Shard 2 ─────► Coordinator: Returns JSON body.
```

## Build it
See `code/query_then_fetch_sim.py` demonstrating network byte savings in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/45-query-then-fetch/experiments/run_experiment.sh
```

## Inspect it
Trace search phases using the `_profile` API:
```bash
curl -X POST http://localhost:9200/products_phase06/_search -H "Content-Type: application/json" -d '{
  "profile": true,
  "query": { "match": { "title": "keyboard" } }
}'
```

## Measure it
Compare total network bytes transferred under Query-Then-Fetch vs an eager full-document fetch.

## Break it
Request `from: 10000, size: 10000` (deep pagination): each shard must score and send 20,000 IDs to the coordinator, exhausting coordinator heap memory.

## Recover it
Enforce `index.max_result_window: 10000` (default safety limit) and migrate deep paging to `search_after`.

## Modify it
Use `stored_fields` or `docvalue_fields` during the fetch phase to retrieve specific attributes without decompressing `_source`.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why does Query-Then-Fetch require two network roundtrips between coordinator and data nodes?
2. What happens during the Fetch phase if one of the winning documents was deleted between the Query and Fetch phases?

## Guarantees
* Maximizes network efficiency by transferring full document payloads only for winning hits.

## Non-guarantees
* Does not eliminate deep pagination sorting overhead (since all candidate IDs up to `from + size` must be collected).

## When to use this
* Default distributed search across all Elasticsearch indices.

## When not to use this
* Single-shard indices (Elasticsearch automatically optimizes single-shard queries).

## What comes next
In Phase 46, we analyze Shard Count sizing and benchmarking.
