# Lesson 129: Input Size Limits

> **Motto**: Enforcing strict input size limits prevents attackers from exhausting server memory and disk with oversized payloads.

---

## Motto
"Enforcing strict input size limits prevents attackers from exhausting server memory and disk with oversized payloads."

## Problem
Accepting unbounded JSON bodies allows an attacker to send a 500MB JSON string, consuming RAM and crashing the server with OOM.

## Prediction
Rejecting payloads exceeding size thresholds (e.g. max 1MB for JSON, max 10MB for uploads) with HTTP 413 stops Denial of Service.

## Why this matters
Input size boundaries protect memory, network buffers, and parser CPU from resource exhaustion attacks.

## First principles
Client Request -> Check Content-Length > MaxLimit? YES: Return 413 Payload Too Large immediately without reading body!

## Mental model
```text
Incoming HTTP Request ──[Content-Length: 150MB]──> Ingress Limit (Max: 10MB) ──[413 Payload Too Large]──> Dropped immediately!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Nginx `client_max_body_size` and ASGI streaming payload limiters.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/129-input-size-limits/tests/ -v
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
- **Failure Injection**: Send a 20MB POST request to an endpoint configured for a 1MB limit; observe immediate HTTP 413 rejection.
- Execute the experiment script:
```bash
python phases/129-input-size-limits/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that the server drops the connection before reading the entire 20MB into process memory.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Check both the `Content-Length` header AND enforce a streaming byte counter: malicious clients can omit the header.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Configure input size limits at the reverse proxy (Nginx `client_max_body_size`) as the first line of defense.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Enforce distinct limits for distinct routes: allow larger limits for file uploads, strict small limits for JSON APIs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must a server verify the streaming byte count even if the `Content-Length` header claims to be small?
2. What HTTP status code specifically indicates that the request payload exceeds server limits?
3. Why is rejecting oversized requests at the reverse proxy superior to rejecting them in application Python code?

## What comes next
Having understood input size limits, we next discover its inherent boundaries and transition to **Abuse and Resource Exhaustion**.
