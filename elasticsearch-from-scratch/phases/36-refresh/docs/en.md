# Lesson 36.1: Refresh

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
