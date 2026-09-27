# Lesson 68.1: Ingest Pipelines

## Motto
"Transform data before indexing: Grok parsing, date conversion, renaming, and geo-ip lookup at the cluster ingestion boundary."

## Problem
Log shippers and client applications send raw, messy text lines:
`"192.168.1.1 - - [23/Sep/2026:12:00:00] 'GET /api/v1/checkout HTTP/1.1' 200 452"`
If the application must parse regexes, convert timestamps, and extract IP addresses before indexing, every client microservice duplicates complex parsing logic.

## Prediction
Can Elasticsearch parse raw log strings into structured JSON fields during ingestion before the document reaches the index mapping?

## Why this matters
**Ingest Pipelines** execute pre-processing processors on data nodes before documents are validated and indexed into Lucene.

## First principles
Ingest Node Processors:
* `grok`: Parses unstructured log strings into structured fields using regular expressions.
* `date`: Parses custom timestamp formats into standard ISO 8601 `@timestamp`.
* `rename`: Modifies field names.
* `set`: Assigns default values.
* `geoip`: Translates IP addresses into geographic latitude, longitude, and country.

## Mental model
```text
Raw Document: { "raw_line": "10.0.0.1 GET /login 200" }
                         │
                 [ Ingest Pipeline ]
                         │
   ├── Grok Processor: extracts ip, method, endpoint, status
   ├── Convert Processor: casts status to integer
   └── Remove Processor: drops raw_line
                         │
                         ▼
Indexed Document: { "ip": "10.0.0.1", "endpoint": "/login", "status": 200 }
```

## Build it
See `code/ingest_pipeline_sim.py` demonstrating pipeline transformations in Python.

## Use Elasticsearch
Run the experiment:
```bash
./phases/68-ingest-pipelines/experiments/run_experiment.sh
```

## Inspect it
Create an ingest pipeline using `_ingest/pipeline`:
```bash
curl -X PUT http://localhost:9200/_ingest/pipeline/parse_access_logs -H "Content-Type: application/json" -d '{
  "description": "Extracts fields from access log",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["%{IP:client_ip} %{WORD:http_method} %{URIPATH:request_path} %{NUMBER:status_code:int}"]
      }
    }
  ]
}'
```
Test the pipeline with `_simulate`:
```bash
curl -X POST http://localhost:9200/_ingest/pipeline/parse_access_logs/_simulate -H "Content-Type: application/json" -d '{
  "docs": [
    { "_source": { "message": "192.168.1.50 GET /cart/checkout 200" } }
  ]
}'
```

## Measure it
Inspect CPU overhead on ingest nodes during heavy Grok regex parsing.

## Break it
Pass a malformed string that fails Grok parsing without an `on_failure` handler. Indexing fails with `grok_parse_failure`!

## Recover it
Add an `on_failure` processor block to route failed logs to an error field or dead-letter index.

## Modify it
Set `default_pipeline` in index settings so all writes to the index automatically pass through the pipeline.

## Evidence
Record observations in [outputs/evidence-template.md](../outputs/evidence-template.md).

## Questions for mastery
1. Why is running `_simulate` recommended before applying an Ingest Pipeline to production data?
2. What are the trade-offs of preprocessing logs in Elasticsearch ingest nodes vs upstream in Logstash or Vector?

## Guarantees
* Documents are fully transformed before entering the mapping and indexing stage.

## Non-guarantees
* Complex Grok regexes can consume high CPU if expressions trigger catastrophic backtracking.

## When to use this
* Lightweight log transformation, field normalization, and IP geolocations.

## When not to use this
* Heavy ETL requiring distributed stream joins or multi-sink routing (use Apache Flink or Kafka Streams).

## What comes next
In Phase 69, we design our application-facing Search API.
