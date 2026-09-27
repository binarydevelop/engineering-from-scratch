# Lesson 143: Cache as Derived Data

> **Motto**: A cache is disposable derived data; the system must function correctly and recover if the entire cache is instantly wiped.

---

## Motto
"A cache is disposable derived data; the system must function correctly and recover if the entire cache is instantly wiped."

## Problem
Treating Redis as an authoritative primary datastore causes permanent data loss when Redis restarts or evicts keys under memory pressure.

## Prediction
Designing caches as ephemeral projections of the primary database ensures the cache can be flushed at any second without data loss.

## Why this matters
Understanding cache dispensability prevents catastrophic architectural data loss and simplifies operational recovery.

## First principles
Primary DB = Authoritative Source of Truth (Durable, ACID). Cache = Ephemeral Performance Optimization (Derived, Disposable).

## Mental model
```text
Redis FLUSHALL (Entire Cache Wiped) -> System slows down temporarily -> Rebuilds cache on demand -> ZERO DATA LOST!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Cache-aside architecture with automated cold-cache rebuilding.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/143-cache-as-derived-data/tests/ -v
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
- **Failure Injection**: Wipe the entire cache store while running active read/write traffic.
- Execute the experiment script:
```bash
python phases/143-cache-as-derived-data/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that all endpoints continue functioning correctly via database queries and automatically repopulate the cache.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Configure Redis eviction policies appropriately: `volatile-lru` or `allkeys-lru` when using Redis as a cache.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never store data in Redis that cannot be reconstructed from the primary database or external sources unless Redis is explicitly configured as a durable store.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Cache warming: after wiping a large production cache, run background warming scripts to avoid overwhelming databases.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What does it mean to treat a cache as 'derived data'?
2. What happens to an application when its Redis cache is completely wiped if the cache was correctly designed?
3. What disaster occurs if an application treats an ephemeral Redis instance as its authoritative source of truth?

## What comes next
Having understood cache as derived data, we next discover its inherent boundaries and transition to **Data Consistency Across Systems**.
