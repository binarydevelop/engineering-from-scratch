# Lesson 07: Headers

> **Motto**: HTTP headers are metadata key-value pairs that govern content negotiation, caching, authentication, and security boundaries.

---

## Motto
"HTTP headers are metadata key-value pairs that govern content negotiation, caching, authentication, and security boundaries."

## Problem
Treating headers as incidental leads to encoding bugs, MIME confusion, and security leaks.

## Prediction
Setting Content-Type: application/json tells the client parser how to decode wire bytes.

## Why this matters
Headers control security policies (CSP, CORS), client caching, and distributed tracing.

## First principles
Headers are colon-separated ASCII key-values terminated by CRLF, case-insensitive per RFC 9110.

## Mental model
```text
Request Headers (Intent/Auth) + Response Headers (Instructions/Policy) + Representation Headers (MIME/Length)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI Header parameters, Response headers, and Starlette Headers wrapper.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/07-headers/tests/ -v
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
- **Failure Injection**: Send incompatible Accept header or missing Content-Type on POST payload.
- Execute the experiment script:
```bash
python phases/07-headers/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Server detects negotiation failure and returns 406 Not Acceptable or 415 Unsupported Media Type.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement header whitelisting and automated security header injection.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Header injection: unvalidated user input written into response headers can lead to HTTP response splitting.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Reverse proxies strip hop-by-hop headers (Connection, Keep-Alive) while forwarding end-to-end headers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why are HTTP header names case-insensitive?
2. What is the difference between Content-Type and Accept headers?
3. How does the Idempotency-Key header protect payment requests?

## What comes next
Having understood headers, we next discover its inherent boundaries and transition to **JSON APIs**.
