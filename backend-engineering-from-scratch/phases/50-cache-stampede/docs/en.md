# Lesson 50: Cache Stampede

> **Motto**: A cache stampede (thundering herd) occurs when a hot cache key expires, causing hundreds of concurrent requests to hammer the database.

---

## Motto
"A cache stampede (thundering herd) occurs when a hot cache key expires, causing hundreds of concurrent requests to hammer the database."

## Problem
When an expired key is requested by 500 simultaneous clients, all 500 experience a cache miss and run expensive queries at once.

## Prediction
Implementing single-flight mutex locking or probabilistic early expiration ensures only one query regenerates the cache.

## Why this matters
Cache stampedes cause sudden, catastrophic database CPU spikes and connection pool exhaustion during peak traffic.

## First principles
Hot Key Expires -> 500 Concurrent Requests Miss -> 500 Identical SQL Queries -> Database Crashes.

## Mental model
```text
Hot Key Miss -> Acquire Distributed Lock -> Winner queries DB & refills Cache -> Other 499 wait or read slightly stale
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Single-flight locking mechanisms protecting hot cache keys.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/50-cache-stampede/tests/ -v
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
- **Failure Injection**: Expire a hot key while sending 100 concurrent async requests; count queries hitting the database.
- Execute the experiment script:
```bash
python phases/50-cache-stampede/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Without protection: 100 queries hit DB. With single-flight mutex: exactly 1 query hits DB; 99 wait and share the result.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Add randomized TTL jitter (`TTL = base_ttl + random(0, 30)`) so related keys do not all expire at the exact same second.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Stampedes can crash databases even when total application traffic is well within normal operating thresholds.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Pre-warming caches and running background refresh tasks eliminates cache stampedes on critical catalog pages.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a cache stampede and why does it occur when a hot key expires?
2. How does a Single-Flight or Mutex pattern protect the database during a cache miss storm?
3. Why should cache TTLs always include randomized jitter?

## What comes next
Having understood cache stampede, we next discover its inherent boundaries and transition to **Background Work Problem**.
