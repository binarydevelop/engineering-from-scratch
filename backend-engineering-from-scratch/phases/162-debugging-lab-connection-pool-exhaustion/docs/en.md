# Lesson 162: Debugging Lab: Connection Pool Exhaustion

> **Motto**: Diagnosing connection pool exhaustion involves identifying connection leaks in exception paths or long-running transactions.

---

## Motto
"Diagnosing connection pool exhaustion involves identifying connection leaks in exception paths or long-running transactions."

## Problem
When all database connections become saturated, the entire application freezes; restarting the server only clears symptoms temporarily.

## Prediction
Tracing active checked-out connections and reviewing exception paths reveals the unreleased connection leak.

## Why this matters
Resolving connection leaks permanently stabilizes database-backed backend services under sustained load.

## First principles
Pool Max = 10. Handler acquires connection -> Crashes without finally block -> Connection leaked. After 10 crashes: TOTAL FREEZE.

## Mental model
```text
Request 11 -> Pool.acquire() -> [No connections available] -> Waits pool_timeout (5s) -> 500 PoolTimeoutError!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Connection pool telemetry and active session diagnostics.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/162-debugging-lab-connection-pool-exhaustion/tests/ -v
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
- **Failure Injection**: Trigger the leaking endpoint 10 times; observe all subsequent requests hang and fail with pool timeout errors.
- Execute the experiment script:
```bash
python phases/162-debugging-lab-connection-pool-exhaustion/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect active connection count; identify connection leak in missing exception cleanup; refactor with context manager.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Connection pool exhaustion creates sudden, total application failure where all endpoints stop responding simultaneously.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Always wrap connection acquisition in context managers (`with` statements) to guarantee release on all exit paths.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Monitor pool checkout duration: alert if connections remain checked out for longer than 10 seconds.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the symptoms of database connection pool exhaustion from the client perspective?
2. How does an unhandled exception inside a database handler cause a connection leak if not wrapped in a context manager?
3. What monitoring metrics should be configured to detect connection pool exhaustion before a total outage occurs?

## What comes next
Having understood debugging lab: connection pool exhaustion, we next discover its inherent boundaries and transition to **Debugging Lab: Redis Down**.
