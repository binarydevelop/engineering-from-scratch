# Lesson 166: Debugging Lab: Stale Cache

> **Motto**: Diagnosing stale data bugs involves tracing missing or misnamed cache invalidation calls following database update mutations.

---

## Motto
"Diagnosing stale data bugs involves tracing missing or misnamed cache invalidation calls following database update mutations."

## Problem
A user updates their email or product price, but the application continues returning the old data for hours.

## Prediction
Comparing database records with cached values and auditing write-path invalidation hooks reveals the missing eviction.

## Why this matters
Ensuring cache invalidation consistency eliminates baffling customer reports of stale or corrupted data.

## First principles
Update Endpoint: Updates PostgreSQL -> FORGETS `cache.delete(key)` -> Cache remains old -> Stale data bug!

## Mental model
```text
POST /products/1 (Price: $20) -> SQL updated -> Redis still holds $10 -> GET /products/1 returns $10 (Stale Data!)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Cache invalidation auditing and cache-key consistency verification.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/166-debugging-lab-stale-cache/tests/ -v
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
- **Failure Injection**: Execute update request; query GET endpoint; observe stale value returned because cache key was not evicted.
- Execute the experiment script:
```bash
python phases/166-debugging-lab-stale-cache/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect write-path code; identify missing cache deletion; add post-commit invalidation; verify GET returns fresh data immediately.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Cache key naming bugs: updating `product:1` while the read path queries `prod:1` causes invalidation to miss the target.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Always invalidate caches *after* the database transaction commits successfully to avoid race conditions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Set sensible TTLs on all cached keys as an ultimate safety net against missing invalidation bugs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What causes an API to return stale data when the primary database already contains updated records?
2. Why do cache key naming discrepancies (e.g. `user:1` vs `users:1`) create silent cache invalidation failures?
3. Why does setting a fallback TTL on every cache key act as a critical safety net?

## What comes next
Having understood debugging lab: stale cache, we next discover its inherent boundaries and transition to **Debugging Lab: Database Lock**.
