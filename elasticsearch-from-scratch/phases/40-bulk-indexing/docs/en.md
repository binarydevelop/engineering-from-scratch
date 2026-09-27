# Lesson 40.1: Bulk Indexing

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
