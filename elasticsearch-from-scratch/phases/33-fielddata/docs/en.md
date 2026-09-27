# Lesson 33.1: Fielddata

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
