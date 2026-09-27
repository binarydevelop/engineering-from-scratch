# Lesson 161: Debugging Lab: 500 Errors

> **Motto**: Diagnosing a sudden spike in HTTP 500 errors requires correlating request IDs across structured logs and stack traces.

---

## Motto
"Diagnosing a sudden spike in HTTP 500 errors requires correlating request IDs across structured logs and stack traces."

## Problem
When 500 errors spike in production, developers stare at logs without a plan, overwhelmed by millions of text lines.

## Prediction
Filtering by `level=ERROR`, grouping by exception type, and tracing correlation IDs pinpoints unhandled edge cases.

## Why this matters
Disciplined exception triage isolates software bugs rapidly without causing secondary outages.

## First principles
500 Spike Alert -> Filter logs by `level=ERROR` -> Group by Exception Signature -> Trace Request ID -> Isolate Bug.

## Mental model
```text
Alert: 500 Error Spike -> Log Search: `level:ERROR` -> Traceback: `AttributeError: 'NoneType' object has no attribute 'price'`
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Structured log analysis and exception handling.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/161-debugging-lab-500-errors/tests/ -v
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
- **Failure Injection**: Send a batch of requests containing edge-case null values; observe 500 error spike in metrics.
- Execute the experiment script:
```bash
python phases/161-debugging-lab-500-errors/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Extract `X-Request-ID` from error response; search logs; locate exact traceback and failing code line; apply defensive fix.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: HTTP 500 errors indicate unhandled bugs; well-designed APIs catch domain failures and return appropriate 4xx status codes.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never let unhandled exceptions leak raw Python tracebacks to external clients in production responses.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Group exceptions by fingerprint in tools like Sentry to identify high-frequency bugs instantly.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference in meaning between an HTTP 4xx error and an HTTP 5xx error?
2. How does a Request Correlation ID allow you to isolate a single failing transaction out of millions of log lines?
3. Why should unhandled exceptions be caught globally and converted into sanitized RFC 9457 Problem Details responses?

## What comes next
Having understood debugging lab: 500 errors, we next discover its inherent boundaries and transition to **Debugging Lab: Connection Pool Exhaustion**.
