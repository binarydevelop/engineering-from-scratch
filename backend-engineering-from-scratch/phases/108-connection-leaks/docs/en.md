# Lesson 108: Connection Leaks

> **Motto**: Connection leaks occur when database connections or sockets are checked out from a pool but never returned, starving the service.

---

## Motto
"Connection leaks occur when database connections or sockets are checked out from a pool but never returned, starving the service."

## Problem
An unhandled exception inside a database handler that lacks a `finally` block leaves the connection checked out indefinitely.

## Prediction
After 20 such errors, an entire pool of 20 connections is permanently exhausted, causing all subsequent user requests to hang and time out.

## Why this matters
Placing connection acquisition inside strict context managers guarantees connections are returned regardless of errors.

## First principles
Acquire Connection -> Exception Raised -> Finally Block NOT EXECUTED -> Connection Leaked -> Pool Starvation.

## Mental model
```text
Normal: Pool.acquire() -> Query -> Pool.release() | Leaked: Pool.acquire() -> Crash! -> Connection lost forever in limbo
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SQLAlchemy / asyncpg context managers (`async with pool.acquire():`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/108-connection-leaks/tests/ -v
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
- **Failure Injection**: Trigger 10 exceptions in an endpoint that forgets to release connections; observe subsequent requests time out waiting for pool.
- Execute the experiment script:
```bash
python phases/108-connection-leaks/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect pool metrics: active connections = 10, idle connections = 0; pool completely frozen.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Refactor code to use context managers (`with` / `async with`); verify connections are 100% released even on exceptions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Configure connection pool acquisition timeouts (e.g. 5 seconds) so requests fail fast rather than hanging indefinitely.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Monitor active checked-out connections vs pool capacity; alert if checked-out connections remain elevated while idle.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What causes a database connection leak in application code?
2. Why does a connection leak in an exception handling branch eventually crash the entire backend service?
3. How do Python context managers (`with` statements) prevent connection leaks mechanically?

## What comes next
Having understood connection leaks, we next discover its inherent boundaries and transition to **Timeout Cascades**.
