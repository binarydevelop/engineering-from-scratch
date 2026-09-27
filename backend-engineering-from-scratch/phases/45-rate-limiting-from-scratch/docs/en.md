# Lesson 45: Rate Limiting From Scratch

> **Motto**: Rate limiting bounds request volume per client, protecting backend services from abuse, brute-force, and resource exhaustion.

---

## Motto
"Rate limiting bounds request volume per client, protecting backend services from abuse, brute-force, and resource exhaustion."

## Problem
Unthrottled endpoints allow attackers to flood CPU-heavy routes, guess passwords, or exhaust database connections.

## Prediction
Implementing in-memory token bucket or fixed-window rate limiters rejects abusive traffic with HTTP 429.

## Why this matters
Rate limiting is essential for system stability, fair resource sharing, and financial defense against DDoS.

## First principles
Token Bucket: Bucket holds $B$ tokens, refills at $R$ tokens/second. Request consumes 1 token. Empty bucket -> 429.

## Mental model
```text
Request Arrives -> Check Bucket(Client IP) -> Token Available? YES: Decrement & Proceed | NO: Return 429 Too Many Requests
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SlowAPI and FastAPI rate limiting middleware integration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/45-rate-limiting-from-scratch/tests/ -v
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
- **Failure Injection**: Send 15 requests in 100 milliseconds against an endpoint configured for 10 requests/minute burst.
- Execute the experiment script:
```bash
python phases/45-rate-limiting-from-scratch/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: First 10 requests succeed (200 OK); subsequent requests are rejected with HTTP 429 and `Retry-After` header.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Include standard rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Rate limiting by IP alone can unfairly throttle entire corporate offices sharing a single NAT gateway; combine with User ID.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: In-memory rate limiters do not share state across multiple backend replicas; distributed rate limiting is needed.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does the Token Bucket algorithm differ from a Fixed Window rate limiting algorithm?
2. What HTTP status code and header must a rate limiter return when quota is exhausted?
3. What happens to an in-memory rate limiter when application traffic is distributed across 5 container replicas?

## What comes next
Having understood rate limiting from scratch, we next discover its inherent boundaries and transition to **Distributed Rate Limiting**.
