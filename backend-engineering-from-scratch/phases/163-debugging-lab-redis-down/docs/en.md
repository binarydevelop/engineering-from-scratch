# Lesson 163: Debugging Lab: Redis Down

> **Motto**: Diagnosing and surviving a cache outage requires implementing graceful fail-open degradation to the primary database.

---

## Motto
"Diagnosing and surviving a cache outage requires implementing graceful fail-open degradation to the primary database."

## Problem
When Redis crashes, an unhardened application throws unhandled `ConnectionRefusedError` and returns 500 for all user requests.

## Prediction
Wrapping cache calls in try-fallback blocks allows the service to fail open, reading from the database and staying online.

## Why this matters
Fail-open caching ensures that an outage in an auxiliary cache node never brings down the primary business service.

## First principles
Redis Down -> Cache.get() raises ConnectionError -> CATCH & LOG -> Fall back to SQL Database -> Return 200 OK!

## Mental model
```text
Redis Crashes ──[Connection Refused]──> Cache Client catches error ──> Queries PostgreSQL ──> Returns 200 OK to User
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Resilient caching middleware and circuit breakers for Redis.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/163-debugging-lab-redis-down/tests/ -v
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
- **Failure Injection**: Terminate the Redis service while running continuous traffic against a cached endpoint.
- Execute the experiment script:
```bash
python phases/163-debugging-lab-redis-down/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Unhardened code crashes with 500 errors; apply fail-open fallback; verify endpoint continues serving 200 OK via database.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Fail-open vs Fail-closed: fail open for non-critical caches (catalog reads); fail closed for security caches (rate limiting).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Log cache connection failures at `WARNING` level with rate-limiting to avoid flooding logs during prolonged Redis outages.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Be aware that failing open to the database during peak traffic can overwhelm the database with sudden un-cached traffic.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between 'fail-open' and 'fail-closed' behavior during a caching infrastructure outage?
2. Why should an application never allow an unhandled Redis connection exception to return HTTP 500 to users?
3. What risk does failing open to the primary database create during peak traffic periods?

## What comes next
Having understood debugging lab: redis down, we next discover its inherent boundaries and transition to **Debugging Lab: Worker Lag**.
