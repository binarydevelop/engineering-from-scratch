# Lesson 93: Tracing

> **Motto**: Distributed tracing tracks the exact execution path of a request across networks, processes, and database queries as a tree of spans.

---

## Motto
"Distributed tracing tracks the exact execution path of a request across networks, processes, and database queries as a tree of spans."

## Problem
When an API takes 3.8 seconds to respond, logs and metrics show that it was slow, but cannot pinpoint which specific query or call hung.

## Prediction
Tracing breaks a request into timed Spans (HTTP -> Auth -> DB Query -> Payment Gateway), exposing the bottleneck immediately.

## Why this matters
Distributed tracing is the ultimate tool for debugging latency anomalies in complex distributed architectures.

## First principles
Trace = Root Span (HTTP Request) -> Child Span 1 (SQL Query) -> Child Span 2 (Redis GET) -> Child Span 3 (External API).

## Mental model
```text
Root Span: GET /orders (350ms)
├── Child Span: Auth Middleware (5ms)
├── Child Span: SQL SELECT (12ms)
└── Child Span: Stripe Charge API (330ms) <── BOTTLENECK IDENTIFIED!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: OpenTelemetry Python SDK and ASGI trace middleware integration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/93-tracing/tests/ -v
```

## Inspect it
Observe state directly using operating system, network, or database inspection:
- Inspect raw bytes, socket buffers, or table schemas
- Verify that request transformations match protocol specifications

## Measure it
Quantify latency and resource consumption:
- Measure response latency percentiles (p50, p95, p99)
- Profile memory allocations and database connection usage under load

## Break it
Inject an intentional failure to observe divergence from expected behavior:
- **Failure Injection**: Execute a request that performs an internal sleep inside a database span; inspect the generated trace hierarchy.
- Execute the experiment script:
```bash
python phases/93-tracing/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe trace tree output; verify that the visual span breakdown immediately highlights the slow database span.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Propagate trace context across HTTP boundaries using the W3C `traceparent` standard header.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Trace sampling: tracing 100% of production traffic generates massive storage overhead; sample 1-5% of normal traffic and 100% of errors.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Attach useful metadata attributes (SQL query text, HTTP status, tenant ID) to spans to facilitate filtering.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between a Trace and a Span in distributed tracing?
2. How does the W3C `traceparent` header propagate context across independent microservices?
3. Why do production distributed tracing systems use trace sampling instead of recording 100% of requests?

## What comes next
Having understood tracing, we next discover its inherent boundaries and transition to **RED Method**.
