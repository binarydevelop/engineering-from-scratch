# Lesson 48: Cache-Aside

> **Motto**: Cache-Aside (Lazy Loading) reads from cache on demand and populates missing keys from the primary database.

---

## Motto
"Cache-Aside (Lazy Loading) reads from cache on demand and populates missing keys from the primary database."

## Problem
Complex caching architectures that update cache synchronously on every write introduce race conditions and code bloat.

## Prediction
Cache-Aside ensures that only requested data is cached, memory is utilized efficiently, and cache node crashes are tolerated.

## Why this matters
Cache-Aside is the universal default caching pattern for web applications and microservices.

## First principles
Read: Cache.get(k) -> Miss -> DB.query(k) -> Cache.set(k, v, TTL) -> Return. Write: DB.update(k) -> Cache.delete(k).

## Mental model
```text
Request -> 1. Cache GET -> [MISS] -> 2. SQL SELECT -> 3. Cache SETEX (key, 60s, data) -> Return Response
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI endpoint integrating Redis cache-aside caching.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/48-cache-aside/tests/ -v
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
- **Failure Injection**: Query an item for the first time (Cache Miss: DB query logged); query a second time (Cache Hit: 0 DB queries).
- Execute the experiment script:
```bash
python phases/48-cache-aside/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify database query logs confirm zero SQL queries executed on subsequent requests.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always set an explicit Time-To-Live (TTL) on every cached key to guarantee eventual consistency.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Cache keys must include tenant and user scoping (`tenant:123:user:45:profile`) to prevent cross-tenant data leaks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: If the cache service crashes, Cache-Aside allows the application to gracefully fall back to querying the database.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the exact sequential steps of a Cache-Aside read path?
2. Why should cache keys always have an explicit TTL?
3. How does Cache-Aside handle a total outage of the Redis caching cluster?

## What comes next
Having understood cache-aside, we next discover its inherent boundaries and transition to **Cache Invalidation**.
