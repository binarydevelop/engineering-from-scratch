# OpenTelemetry Collector Pipelines Architecture

> **Motto**: The Collector is the central nervous system of modern telemetry; without memory limiters and batching, it becomes your first point of catastrophic failure.

---

## 1. The Anatomy of an OTel Pipeline

Every pipeline in the OpenTelemetry Collector processes telemetry through a strictly ordered linear sequence:

```text
[ Receivers ]  ──►  [ Processors ]  ──►  [ Exporters ]
  - otlp (gRPC/HTTP)  - memory_limiter   - prometheus (metrics)
  - prometheus        - transform        - otlp/tempo (traces)
                      - batch            - debug (stdout)
```

### The Three Pipeline Stages
1. **Receivers**: Push or pull data into the Collector. Receivers convert incoming payloads into internal OpenTelemetry in-memory models (`pdata`).
2. **Processors**: Manipulate, filter, sample, or buffer telemetry. Processors execute in the exact order declared in `service.pipelines`.
3. **Exporters**: Translate internal `pdata` structures into target backend formats (Prometheus, OTLP, Elasticsearch, Jaeger).

---

## 2. Critical Processor Invariants

### 1. `memory_limiter` MUST be the First Processor
If `memory_limiter` is placed after `batch` or `transform`, the Collector will buffer incoming payloads in memory before checking limits, causing the Linux kernel OOM killer to terminate the Collector process.

### 2. The `batch` Processor is Non-Negotiable
Without batching, every individual span or log line triggers an independent network round-trip to the storage backend, wasting CPU cycles on serialization and choking network buffers.
