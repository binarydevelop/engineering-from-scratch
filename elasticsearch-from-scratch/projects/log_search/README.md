# Capstone 2: Structured Log Search & APM Analytics

A scalable microservices log search, error aggregation, and telemetry engine in Elasticsearch 8.17.0.

---

## 1. Features
* **Time-Series Log Model:** Structured documents indexed with `@timestamp`, `service`, `level`, `trace_id`, `status_code`, and `duration_ms`.
* **Multi-Tier Aggregations:** Groups errors by service, extracts top recurring failure messages, and computes streaming p95 latency percentiles using T-Digest.
* **Trace ID Correlation:** Exact lookup of distributed trace spans across microservices.

---

## 2. Usage Instructions

```bash
# 1. Ingest synthetic microservice log events
python3 projects/log_search/generator.py

# 2. Run incident diagnosis and error rate analytics report
python3 projects/log_search/analyzer.py
```
