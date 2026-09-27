# Lesson 46: Distributed Rate Limiting

> **Motto**: Distributed rate limiting coordinates request quotas across multiple application nodes using a shared, atomic datastore.

---

## Motto
"Distributed rate limiting coordinates request quotas across multiple application nodes using a shared, atomic datastore."

## Problem
In-memory rate limiters reset on node restarts and allow clients to bypass quotas by hitting different server replicas.

## Prediction
Using Redis with atomic Lua scripts or sliding window logs enforces strict global rate limits across all nodes.

## Why this matters
Distributed rate limiting protects multi-node production clusters from synchronized botnets and brute-force spikes.

## First principles
Replicas A, B, C -> Shared Redis Datastore (Atomic Lua Script) -> Enforces Global Limit.

## Mental model
```text
Request hits Replica 2 -> Redis EVAL (Sliding Window Log) -> Atomic Increment & Check -> Return Global Quota
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Redis-backed rate limiting in FastAPI using token bucket or sliding window algorithms.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/46-distributed-rate-limiting/tests/ -v
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
- **Failure Injection**: Send concurrent requests distributed across 3 distinct server instances targeting the same client key.
- Execute the experiment script:
```bash
python phases/46-distributed-rate-limiting/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe global request counter increment atomically across nodes; all nodes enforce limit simultaneously.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use Redis Lua scripts (`EVAL`) to combine checking, incrementing, and setting TTL into a single atomic roundtrip.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Redis failure mode: decide whether the rate limiter should 'fail open' (allow traffic) or 'fail closed' (reject traffic) if Redis goes down.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: High-throughput APIs often use local memory caching with periodic asynchronous batch sync to reduce Redis network load.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why do multiple server instances require atomic Redis operations (like Lua scripts) for rate limiting?
2. What is the difference between 'fail-open' and 'fail-closed' when a rate-limiting datastore crashes?
3. How does a Sliding Window Log prevent boundary burst exploitation compared to Fixed Window?

## What comes next
Having understood distributed rate limiting, we next discover its inherent boundaries and transition to **Why Caching Exists**.
