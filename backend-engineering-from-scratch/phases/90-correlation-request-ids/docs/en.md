# Lesson 90: Correlation / Request IDs

> **Motto**: A Correlation ID tracks a single logical transaction across multiple microservices, background workers, and log records.

---

## Motto
"A Correlation ID tracks a single logical transaction across multiple microservices, background workers, and log records."

## Problem
When an API error occurs across 5 distributed services, matching logs without a shared ID is nearly impossible.

## Prediction
Generating a unique `X-Request-ID` at ingress and propagating it across all calls ties disparate logs into one cohesive story.

## Why this matters
Correlation IDs are the fundamental prerequisite for effective distributed debugging and incident response.

## First principles
Client Request (X-Request-ID: abc) -> Ingress -> Service A (Logs with abc) -> Service B (Logs with abc) -> Worker (Logs with abc).

## Mental model
```text
Client ──[X-Request-ID: 7b9d]──> API Gateway ──[7b9d]──> Service A ──[7b9d]──> Service B (All logs tagged 7b9d)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: ContextVars-based request ID propagation in FastAPI and HTTPX client hooks.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/90-correlation-request-ids/tests/ -v
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
- **Failure Injection**: Make a request without a request ID; verify that the server generates one and returns it in the response headers.
- Execute the experiment script:
```bash
python phases/90-correlation-request-ids/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Make a request with an existing `X-Request-ID`; verify that the server preserves and propagates that exact ID.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Propagate the correlation ID into database query comments (`/* request_id: abc */`) to trace slow SQL queries.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Return the request ID in all client error responses so users can quote it to customer support.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Ensure correlation ID generation uses high-entropy UUIDs (UUIDv4) to guarantee global uniqueness.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a Request Correlation ID and why is it essential in microservice architectures?
2. How does Python's `contextvars` module allow request IDs to be accessed anywhere in code without passing parameters?
3. Why should an API return the `X-Request-ID` in HTTP response headers to clients?

## What comes next
Having understood correlation / request ids, we next discover its inherent boundaries and transition to **Metrics**.
