# Phases 31 – 54: OpenTelemetry Architecture & Pipelines

> **Motto**: Understand it. Instrument it. Measure it. Break it. Detect it. Debug it. Recover it. Automate it. Improve it. Operate it.

---

## Phases 31 – 34: OpenTelemetry Architecture & Identity

### Why OpenTelemetry Exists (Phase 31)
Before OpenTelemetry, every monitoring vendor (Datadog, New Relic, Dynatrace, Honeycomb) forced you to use their proprietary SDK. Switching vendors required ripping out thousands of lines of application code. OpenTelemetry provides a single, CNCF-governed, vendor-neutral standard for telemetry.

### The API vs SDK Boundary (Phase 32)
* **OpenTelemetry API**: Contains interfaces, no-op implementations, and context propagation abstractions. Has zero dependencies and produces zero side effects if no SDK is registered.
* **OpenTelemetry SDK**: Implements in-memory buffering, batching, thread-safety, samplers, and exporters.
* **Rule**: Applications and libraries depend on the API. Only the service entrypoint configures the SDK.

### Semantic Resource Identity (Phase 33)
Using stable OpenTelemetry resource attributes to establish service identity:
```python
resource = Resource.create({
    "service.name": "checkout-service",
    "service.version": "1.4.2",
    "service.instance.id": "pod-checkout-7f9a2",
    "deployment.environment": "production",
})
```

---

## Phases 35 – 40: Tracing & Semantic Conventions

### Stable Semantic Conventions (Phase 37 & 38)
> [!IMPORTANT]
> Deprecated conventions (`http.method`, `http.status_code`) are banned. Stable v1.26+ conventions are enforced:

```python
with tracer.start_as_current_span(
    "POST /checkout",
    attributes={
        "http.request.method": "POST",
        "url.path": "/checkout",
        "server.address": "checkout.internal",
        "server.port": 8001,
    }
) as span:
    # Processing
    span.set_attribute("http.response.status_code", 200)
```

### Database Query Tracing (Phase 39)
```python
with tracer.start_as_current_span(
    "postgresql.query",
    attributes={
        "db.system": "postgresql",
        "db.namespace": "production_store",
        "db.query.text": "SELECT stock FROM inventory WHERE item_id = $1", # Sanitized, no raw literals!
    }
):
    execute_query()
```

---

## Phases 41 – 46: Metrics, Logs, Sampling & OTLP

### Head vs Tail Sampling (Phase 44 & 45)
* **Head Sampling**: Decision made when request begins. E.g., sample 5% of requests. Problem: Rare 500 errors occurring in the other 95% are permanently lost.
* **Tail Sampling**: Collector buffers spans until the trace finishes. Evaluates rule: *Did any span have `status.code == ERROR` or `duration > 1000ms`?* If yes, sample 100%; if no, drop 99% of successful traces.

### OTLP Protocol (Phase 46)
OpenTelemetry Protocol transmits telemetry serialized via Protocol Buffers over:
* **gRPC** (Port 4317): High-throughput binary multiplexed stream with HTTP/2 framing.
* **HTTP/Protobuf or JSON** (Port 4318): For browser clients or network environments blocking gRPC.

---

## Phases 47 – 54: The OpenTelemetry Collector Architecture

### Why You Need a Collector (Phase 47)
Without a Collector, every microservice must manage backend credentials, retry buffers, network backoff, and direct exporter dependencies. The Collector decouples application telemetry from storage infrastructure.

### The Pipeline Execution Order (Phase 48)
```text
Receivers (otlp)
   ↓
Processors (memory_limiter -> transform -> batch)
   ↓
Exporters (prometheus, otlp/tempo, debug)
```

### Collector Under Backend Failure (Phase 52)
When the trace backend (Tempo) crashes:
1. The Collector buffers spans in memory up to its `queued_retry` limit.
2. If `memory_limiter` threshold is reached, the Collector safely drops incoming spans rather than allowing the Linux OOM killer to terminate the Collector process.
3. Once Tempo recovers, queued spans drain automatically without dropping data.
