# Lesson 04: HTTP Request Lifecycle

> **Motto**: Every web request traces an unbroken path from socket descriptor to protocol parser, router, domain logic, and serialized wire return.

---

## Motto
"Every web request traces an unbroken path from socket descriptor to protocol parser, router, domain logic, and serialized wire return."

## Problem
Developers think endpoints execute magically when a URL is requested.

## Prediction
Tracing execution through each transformation reveals the exact cost and latency of each layer.

## Why this matters
When latency spikes or requests fail, knowing the lifecycle lets you locate the bottleneck instantly.

## First principles
A request is an immutable snapshot of client intent transformed into domain operations and serialized back to bytes.

## Mental model
```text
Socket -> Raw Bytes -> HTTP Parser -> Request DTO -> Router -> Handler -> Response DTO -> Serializer -> Socket
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: ASGI middleware stack and route handler execution pipeline.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/04-http-request-lifecycle/tests/ -v
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
- **Failure Injection**: Inject failure at parser stage vs handler stage vs serialization stage.
- Execute the experiment script:
```bash
python phases/04-http-request-lifecycle/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect error response and logs to verify which lifecycle layer caught the failure.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Add lifecycle hooks for timing, error capture, and resource cleanup.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Ensure sensitive request headers (Authorization, Cookie) are redacted before lifecycle logging.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Every layer in the lifecycle adds microsecond overhead; unnecessary middleware multiplies p99 latency.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. At which exact lifecycle stage should authentication be evaluated?
2. What is the operational consequence of an uncaught exception in response serialization?
3. Why must resource cleanup (DB connection return) happen in a finally block?

## What comes next
Having understood http request lifecycle, we next discover its inherent boundaries and transition to **HTTP Methods**.
