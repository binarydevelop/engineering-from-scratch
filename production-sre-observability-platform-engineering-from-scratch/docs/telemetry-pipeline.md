# The Telemetry Pipeline: From First Principles to Storage

> **Motto**: OpenTelemetry is not the database; Prometheus is not the dashboard; a log is not a trace; and sending more telemetry does not make a broken system observable.

---

## 1. The OpenTelemetry Mental Model

One of the most persistent misconceptions in modern software engineering is confusing the telemetry instrumentation and transport pipeline with the storage backends and visualization tools:

```text
       ┌────────────────────────────────────────────────────────┐
       │                Application Process                     │
       │                                                        │
       │   Business Logic                                       │
       │         │                                              │
       │         ▼                                              │
       │   OpenTelemetry API (Language Interface)              │
       │         │                                              │
       │         ▼                                              │
       │   OpenTelemetry SDK (In-Memory Batching & State)       │
       │         │                                              │
       │         ▼                                              │
       │   OTLP Exporter (gRPC / HTTP Protobuf Serialization)   │
       └─────────────────────────┬──────────────────────────────┘
                                 │ OTLP Protocol (Port 4317 / 4318)
                                 ▼
       ┌────────────────────────────────────────────────────────┐
       │             OpenTelemetry Collector                    │
       │                                                        │
       │   Receivers: otlp (Accept incoming streams)            │
       │         │                                              │
       │         ▼                                              │
       │   Processors: memory_limiter, batch, filter, redact    │
       │         │                                              │
       │         ▼                                              │
       │   Exporters: prometheus, tempo, loki, otlp             │
       └──────┬──────────────────┬──────────────────┬───────────┘
              │                  │                  │
              │ Metrics          │ Traces           │ Logs
              ▼                  ▼                  ▼
       ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
       │  Prometheus  │   │ Grafana Tempo│   │ Grafana Loki │
       │ (Time Series)│   │ (Trace Store)│   │ (Log Streams)│
       └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 ▼
       ┌────────────────────────────────────────────────────────┐
       │                        Grafana                         │
       │                 (Visualization Layer)                  │
       └────────────────────────────────────────────────────────┘
```

---

## 2. Core Distinctions You Must Never Forget

| Component | What It IS | What It IS NOT |
|:---|:---|:---|
| **OpenTelemetry (OTel)** | An open standard, API, SDK, and Collector for generating and routing telemetry. | A database, time-series storage, alert engine, or graphing dashboard. |
| **Prometheus** | A pull-based time-series metrics database, PromQL query engine, and alert rule evaluator. | A trace visualizer or centralized log aggregator. |
| **Grafana** | A multi-source query and visualization UI engine. | An observability source; it has zero data of its own. |
| **Grafana Tempo / Jaeger**| A specialized distributed trace storage engine indexing trace IDs and span DAGs. | A metrics aggregator or general log search engine. |
| **Grafana Loki** | A log aggregation engine indexing label metadata rather than full-text tokens. | A replacement for structured trace waterfalls. |

---

## 3. The Signal Selection Framework

When debugging a production anomaly, never jump randomly between tools. Use the **Signal Selection Framework**:

```text
What operational question am I answering?

Need trend, rate, or aggregate behavior?
  ──► METRIC (Prometheus)
      Example: "Did checkout error rate cross 1% after the 14:00 deployment?"

Need causal path across multiple network hops?
  ──► TRACE (Tempo / Jaeger)
      Example: "Why did request #92a4 spend 1.8 seconds inside payment-service?"

Need detailed local state, input parameters, or error stack trace?
  ──► LOG (Loki / Structured JSON)
      Example: "What exact validation payload caused the database driver to throw a syntax error?"

Need CPU hotspot, lock contention, or memory allocation breakdown?
  ──► PROFILE (Continuous Profiling)
      Example: "Which function in the serialization loop is consuming 80% of CPU cycles?"
```

---

## 4. Telemetry Design Discipline

Before writing a single line of instrumentation code or configuring a new exporter, you must answer the **Seven Telemetry Invariants**:

1. **What operational question does this answer?** If you cannot name the exact incident or capacity question, do not instrument it.
2. **Who will use it?** Will an on-call engineer query it at 3 AM, or is it developer curiosity that belongs in local unit tests?
3. **What is the cardinality?** How many unique values will this attribute take? (Never put UUIDs, user IDs, or email addresses into Prometheus metric labels).
4. **What is the expected volume?** What is the data rate in events/sec and megabytes/hour?
5. **Could it expose sensitive data?** Does the payload contain PII, credentials, auth tokens, or private medical/financial data?
6. **What is the retention period?** Do you need this signal for 2 hours (debugging), 30 days (SLO review), or 1 year (compliance)?
7. **What does it cost?** What is the compute, network, and storage overhead imposed on the monitored application and the telemetry collector?
