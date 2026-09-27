# Lesson 182: Project: Rate Limiting Service

> **Motto**: Build a high-performance standalone rate limiting service benchmarking Token Bucket, Sliding Window, and Leaky Bucket algorithms.

---

## Motto
"Build a high-performance standalone rate limiting service benchmarking Token Bucket, Sliding Window, and Leaky Bucket algorithms."

## Problem
Choosing the wrong rate limiting algorithm allows boundary burst exploitation or consumes excessive memory at scale.

## Prediction
Implementing and benchmarking Token Bucket, Fixed Window, and Sliding Window Log algorithms proves their performance tradeoffs.

## Why this matters
Rate limiting services are essential infrastructure for API gateways, DDoS defense, and third-party API monetization.

## First principles
Fixed Window (Fast, burst vulnerability) vs Sliding Window Log (Accurate, high memory) vs Token Bucket (Optimal balance).

## Mental model
```text
Rate Limiter: Inspects Client Key -> Executes Algorithm (Token Bucket / Sliding Window) -> Returns Allowed (True/False, Remaining)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Rate limiting service implementation.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/182-project-rate-limiting-service/tests/ -v
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
- **Failure Injection**: Run comparative benchmark: compare CPU duration and memory footprint of Token Bucket vs Sliding Window under 100,000 requests.
- Execute the experiment script:
```bash
python phases/182-project-rate-limiting-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe Token Bucket executes in < 0.005ms per check with flat memory; Sliding Window provides strict boundary accuracy.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use Redis atomic operations (Lua scripts) to prevent race conditions when executing rate limiting across distributed nodes.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Include standard RFC rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Implement separate rate limit tiers for authenticated users (e.g. 100 RPS) versus unauthenticated IP addresses (e.g. 5 RPS).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the 'boundary burst vulnerability' of the Fixed Window rate limiting algorithm?
2. Why is the Token Bucket algorithm widely preferred for API rate limiting in production systems?
3. How does an atomic Redis Lua script prevent race conditions in distributed rate limiters?

## What comes next
Having understood project: rate limiting service, we next discover its inherent boundaries and transition to **Project: Authentication Service**.
