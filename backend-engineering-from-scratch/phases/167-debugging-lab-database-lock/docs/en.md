# Lesson 167: Debugging Lab: Database Lock

> **Motto**: Diagnosing hanging requests caused by database lock contention requires inspecting active locks in system catalogs.

---

## Motto
"Diagnosing hanging requests caused by database lock contention requires inspecting active locks in system catalogs."

## Problem
Requests hang for 30 seconds before timing out; application CPU is zero; the database is waiting on an uncommitted row lock.

## Prediction
Querying `pg_stat_activity` and `pg_locks` identifies the blocking transaction and the locked table or row.

## Why this matters
Resolving database lock contention prevents cascading connection pool exhaustion and unfreezes blocked traffic.

## First principles
Tx 1: Locks Row A -> Waits on external API (30s). Tx 2: Attempts to update Row A -> BLOCKED waiting for Tx 1 lock!

## Mental model
```text
Tx 1 holds row lock ──> Tx 2 waits ──> Tx 3 waits ──> Connection Pool Exhausted ──> Application Freezes!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: PostgreSQL lock monitoring queries and lock timeout configuration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/167-debugging-lab-database-lock/tests/ -v
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
- **Failure Injection**: Start a transaction that holds a row lock; execute a concurrent update on the same row; observe second request hang.
- Execute the experiment script:
```bash
python phases/167-debugging-lab-database-lock/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Query active locks in the database; locate blocking PID; terminate blocking session; configure `lock_timeout`.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Configure `lock_timeout = '2s'` in PostgreSQL so queries fail fast rather than waiting indefinitely for held locks.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never keep database transactions open while calling external network APIs or performing slow application computation.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: To prevent deadlocks: always acquire row locks in the exact same consistent ordering across all transactions.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How do you identify which database session is blocking other transactions using PostgreSQL system catalogs?
2. Why does holding a database transaction open during a slow external network call create lock contention?
3. How does acquiring locks in a consistent global order prevent database deadlocks?

## What comes next
Having understood debugging lab: database lock, we next discover its inherent boundaries and transition to **Debugging Lab: Disk Full**.
