# Lesson 35.1: Near-Real-Time Search

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
