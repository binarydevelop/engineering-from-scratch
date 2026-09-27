# Part 03: OpenTelemetry (Phases 31 – 54)

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Overview

Part 03 masters the modern OpenTelemetry standard: the API vs SDK separation, stable semantic conventions (v1.26.0+), manual vs automatic instrumentation, metrics, logs, sampling, OTLP transport, and the OpenTelemetry Collector architecture.

---

## Phases in Part 03

| Phase Range | Core Topic | Key Lessons & Invariants |
|:---|:---|:---|
| **Phases 31 – 34** | Architecture & Standards | Why OTel?, API vs SDK separation, Resource identity (`service.name`), Instrumentation Scope |
| **Phases 35 – 40** | Distributed Tracing & Semantic Conventions | Manual tracing, Auto-instrumentation, Semantic conventions (HTTP, DB, Messaging) |
| **Phases 41 – 46** | Metrics, Logs & Transport | OTel Metrics, Log Bridge API, Baggage tradeoffs, Head vs Tail Sampling, OTLP Protocol |
| **Phases 47 – 54** | The OpenTelemetry Collector | Collector derivation, Pipelines (Receivers, Processors, Exporters), Failure recovery, Topologies |

---

## The OpenTelemetry Invariant

```text
OpenTelemetry is NOT the storage backend.
OpenTelemetry is NOT the dashboard.
OpenTelemetry provides vendor-neutral APIs, SDKs, and data pipelines.
```
Never use deprecated attribute names (`http.method`, `http.status_code`). Adhere strictly to stable semantic conventions (`http.request.method`, `http.response.status_code`, `url.path`, `server.address`).
