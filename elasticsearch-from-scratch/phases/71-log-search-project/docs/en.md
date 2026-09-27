# Lesson 71.1: Log Search Project (Capstone 2)

## Motto
"Capstone 2: Structured log aggregation, trace indexing, error histograms, and retention lifecycle."

## Problem
In a microservices cloud architecture with 50 services emitting millions of logs per hour, developers need to diagnose production outages in seconds: "Show all HTTP 500 errors across `payment-service` in the last 15 minutes, group by error message, and correlate with distributed `trace_id`".

## Prediction
How fast can Elasticsearch filter 100,000 logs by service name and aggregate error rates into 1-minute time buckets?

## Why this matters
This capstone covers the operational half of Elasticsearch: high-throughput time-series logging, trace correlation, and analytics dashboards.

## First principles
Log Search Architecture:
1. **Schema:** `@timestamp` (`date`), `service` (`keyword`), `level` (`keyword`), `trace_id` (`keyword`), `message` (`text`), `duration_ms` (`integer`).
2. **Targeted Date Filtering:** Queries ALWAYS bound `@timestamp` to prune index shards.
3. **Facet Aggregations:** `date_histogram` for error rates over time, `terms` on `message.keyword` for top recurring exceptions.

## Mental model
```text
Microservice Fleet (50 pods)
  │ Logs via HTTP/Kafka
  ▼
Elasticsearch Ingest Pipeline ──► Data Stream: logs-app-default
  │
  ├── 1. Filter: service: "payment-service" AND level: "ERROR"
  ├── 2. Aggregation: date_histogram (1m intervals)
  └── 3. Correlate: trace_id = "trace-8891-abc" (Full distributed call stack!)
```

## Build it
See `projects/log_search/` and `code/log_search_engine.py` generating and analyzing structured logs.

## Use Elasticsearch
Run the experiment:
```bash
./phases/71-log-search-project/experiments/run_experiment.sh
```

## Inspect it
Load 5,000 synthetic microservice logs and query for error spikes:
```bash
curl -X POST http://localhost:9200/app_logs/_search -H "Content-Type: application/json" -d '{
  "size": 5,
  "query": {
    "bool": {
      "filter": [
        { "term": { "level": "ERROR" } },
        { "term": { "service": "payment-api" } }
      ]
    }
  },
  "aggs": {
    "errors_per_minute": {
      "date_histogram": { "field": "@timestamp", "fixed_interval": "1m" }
    }
  }
}'
```

## Measure it
Measure query response time for error histogram aggregations (< 10ms).

## Break it
Run an un-bounded text wildcard on `message` without a timestamp filter and observe query duration climb.

## Recover it
Mandate `@timestamp` filters on all log search forms.

## Modify it
Add a percentile aggregation on `duration_ms` to calculate p95 service latency.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is `trace_id` mapped as `keyword` rather than `text`?
2. How does date pruning allow Elasticsearch to skip searching older immutable segments?

## Guarantees
* Provides fast structured filtering and time-series error rate calculations.

## Non-guarantees
* High-volume logging requires capacity planning (Phase 78) to avoid disk exhaustion.

## When to use this
* Centralized logging, distributed tracing (APM), security event auditing (SIEM).

## When not to use this
* Permanent archival where data is never queried (write compressed tarballs to S3 Glacier instead).

## What comes next
In Phase 72, we evaluate search quality using Search Relevance Evaluation metrics.
