# Lesson 49: Cache Invalidation

> **Motto**: There are only two hard things in Computer Science: cache invalidation and naming things.

---

## Motto
"There are only two hard things in Computer Science: cache invalidation and naming things."

## Problem
Updating an entity in the database while leaving stale data in the cache causes users to see outdated prices and corrupted state.

## Prediction
Explicitly evicting cached keys on database mutations guarantees that subsequent reads fetch fresh data.

## Why this matters
Data inconsistency caused by stale caches destroys user trust and creates baffling production bug reports.

## First principles
Write Path: 1. Update Database -> 2. Invalidate / Delete Cache Key -> Subsequent Read triggers fresh Cache-Aside load.

## Mental model
```text
POST /products/1 (Price Update) -> SQL UPDATE -> Redis DEL product:1 -> Next GET /products/1 fetches fresh price
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Database repository with post-commit cache eviction hooks.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/49-cache-invalidation/tests/ -v
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
- **Failure Injection**: Update product price in database without deleting cache; observe GET endpoint returns old price.
- Execute the experiment script:
```bash
python phases/49-cache-invalidation/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Trigger cache eviction (`cache.delete(key)`); observe next GET request returns updated price immediately.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Prefer cache *eviction* (deleting the key) over cache *mutation* (updating the key in Redis) to prevent update race conditions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Ensure cache eviction occurs *after* the database transaction commits, not before, to prevent race conditions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Cache invalidation bugs are notoriously difficult to reproduce; log all cache evictions with timestamps.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is deleting a cached key on update safer than attempting to update the cached value directly?
2. What happens if cache invalidation is executed before the database transaction successfully commits?
3. What is the difference between TTL expiration and explicit event-driven cache invalidation?

## What comes next
Having understood cache invalidation, we next discover its inherent boundaries and transition to **Cache Stampede**.
