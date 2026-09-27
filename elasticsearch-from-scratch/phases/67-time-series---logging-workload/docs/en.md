# Lesson 67.1: Time-Series / Logging Workload

## Motto
"Append-only time-series data requires rolling indices, data streams, and disciplined retention."

## Problem
Logs arrive at 10,000 events/second. If all logs are written into a single monolithic index `app-logs`, the index grows to 20 terabytes. Searching recent logs slows down, and deleting logs older than 30 days requires running a catastrophic `_delete_by_query` that overburdens the cluster with millions of soft deletes!

## Prediction
Why is dropping an entire daily index with `DELETE /logs-2026.01.01` instantaneous and free, whereas deleting 10 million rows with `_delete_by_query` takes hours and bloats disk?

## Why this matters
Time-series architectures leverage filesystem-level directory deletions instead of Lucene row-level tombstones.

## First principles
* **Monolithic Index Anti-Pattern:** A single index cannot easily purge old data. `_delete_by_query` writes `.del` markers, requiring costly segment merges.
* **Rolling Indices / Data Streams:** Data is sliced by time: `logs-2026.01.01`, `logs-2026.01.02`.
* **Deleting Old Data:** Dropping an old index (`DELETE /logs-2025.12.01`) is an instantaneous filesystem directory deletion ($O(1)$) with zero CPU or segment merge overhead!

## Mental model
```text
Bad: Monolithic Index (10 TB)
  Delete 30-day-old logs ──► _delete_by_query ──► 10,000,000 tombstones, high CPU!

Best Practice: Time-Series Indices / Data Stream
  logs-2026-03-21 (Active Hot)
  logs-2026-03-20 (Warm)
  ...
  logs-2025-12-01 (90 days old) ──► DELETE /logs-2025-12-01 ──► Instant directory removal!
```

## Build it
See `code/timeseries_simulator.py` demonstrating time-partitioned log queries in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/67-time-series---logging-workload/experiments/run_experiment.sh
```

## Inspect it
Index a structured log document with a timestamp:
```bash
curl -X POST http://localhost:9200/logs_demo/_doc -H "Content-Type: application/json" -d '{
  "@timestamp": "2026-09-23T12:00:00Z",
  "service": "payment-api",
  "level": "ERROR",
  "status_code": 500,
  "message": "Database connection pool exhausted"
}'
```

## Measure it
Execute a date-histogram aggregation of log errors over time:
```bash
curl -X POST http://localhost:9200/logs_demo/_search -H "Content-Type: application/json" -d '{
  "size": 0,
  "aggs": {
    "errors_over_time": {
      "date_histogram": {
        "field": "@timestamp",
        "fixed_interval": "1h"
      }
    }
  }
}'
```

## Break it
Execute an unbounded search across `logs-*` without a timestamp range filter. Observe query fan-out across dozens of old indices.

## Recover it
Always enforce a `@timestamp` range filter in time-series queries so Elasticsearch can prune non-matching indices before querying shards.

## Modify it
Use modern Elasticsearch Data Streams (`POST /_data_stream/my-data-stream`).

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is dropping a daily index vastly more efficient than running `_delete_by_query`?
2. What is an Elasticsearch Data Stream and how does it manage backing indices?

## Guarantees
* Time-partitioned indices enable instant, zero-cost data retention drops.

## Non-guarantees
* Searching `logs-*` across 1,000 old daily indices will suffer high coordination latency unless pruned by date range.

## When to use this
* Application logs, server metrics, network telemetry, and sensor streams.

## When not to use this
* Entity datasets requiring frequent point updates to existing records (e.g. user profiles).

## What comes next
In Phase 68, we build transformations using Ingest Pipelines.
