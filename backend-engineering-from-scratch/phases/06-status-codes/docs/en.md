# Lesson 06: Status Codes

> **Motto**: HTTP status codes are the universal error protocol of the web; returning 200 for failures destroys client observability.

---

## Motto
"HTTP status codes are the universal error protocol of the web; returning 200 for failures destroys client observability."

## Problem
APIs returning HTTP 200 with `{"status": "error"}` break HTTP proxies, circuit breakers, and monitoring.

## Prediction
Using accurate status codes enables automated client retries, error budgets, and health monitoring.

## Why this matters
Status codes allow edge proxies and CDNs to distinguish client errors (4xx) from server outages (5xx).

## First principles
1xx = Informational, 2xx = Success, 3xx = Redirection, 4xx = Client Error, 5xx = Server/Dependency Error.

## Mental model
```text
Client Error (4xx: Fix your request) vs Server Error (5xx: Fix the server/dependencies)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI HTTPException and exception handlers mapping domain results.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/06-status-codes/tests/ -v
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
- **Failure Injection**: Simulate missing resource, validation error, conflict, and unhandled exception.
- Execute the experiment script:
```bash
python phases/06-status-codes/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify correct mapping to 404, 422, 409, and 500 respectively.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Standardize error payload schema across all non-2xx status codes.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Do not leak internal database errors or stack traces in HTTP 500 response bodies.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Monitoring systems track 5xx rates for alert paging; hiding errors in 200 blinds SRE teams.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. When should an API return 401 Unauthorized vs 403 Forbidden?
2. What is the difference between 400 Bad Request and 422 Unprocessable Entity?
3. What condition warrants returning 409 Conflict?

## What comes next
Having understood status codes, we next discover its inherent boundaries and transition to **Headers**.
