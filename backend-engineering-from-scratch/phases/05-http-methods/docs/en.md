# Lesson 05: HTTP Methods

> **Motto**: HTTP methods are not arbitrary labels; they define the safety, idempotency, and cacheability of distributed operations.

---

## Motto
"HTTP methods are not arbitrary labels; they define the safety, idempotency, and cacheability of distributed operations."

## Problem
Developers use GET for mutations or POST for idempotent updates without understanding distributed consequences.

## Prediction
GET requests can be pre-fetched and retried automatically; POST requests create side effects and cannot be retried blindly.

## Why this matters
Misusing methods causes search crawlers to trigger destructive actions or proxies to cache mutations.

## First principles
RFC 9110 defines: Safe methods do not alter server state; Idempotent methods produce the same state when executed repeatedly.

## Mental model
```text
GET (Safe/Idempotent) | POST (Unsafe/Non-Idempotent) | PUT (Idempotent Replace) | DELETE (Idempotent Remove) | PATCH (Non-Idempotent Partial)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI method decorators (@app.get, @app.post, @app.put, @app.delete, @app.patch).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/05-http-methods/tests/ -v
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
- **Failure Injection**: Send a GET request with a mutating payload and verify architectural rejection.
- Execute the experiment script:
```bash
python phases/05-http-methods/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Catch mutation attempt on safe method and return HTTP 405 Method Not Allowed.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce strict read-only transactions on GET request handlers.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: CSRF attacks exploit safe-method assumptions when browsers trigger automatic GET requests.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: HTTP caches and CDNs only cache safe methods by default; violating semantics pollutes caches.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is DELETE considered idempotent even if the second call returns HTTP 404?
2. What makes PUT different from PATCH mechanically?
3. Why must a search engine crawler never trigger a DELETE or POST?

## What comes next
Having understood http methods, we next discover its inherent boundaries and transition to **Status Codes**.
