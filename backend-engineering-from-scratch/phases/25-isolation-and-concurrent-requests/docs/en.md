# Lesson 25: Isolation and Concurrent Requests

> **Motto**: Concurrent requests modifying the same rows experience isolation anomalies: dirty reads, non-repeatable reads, and lost updates.

---

## Motto
"Concurrent requests modifying the same rows experience isolation anomalies: dirty reads, non-repeatable reads, and lost updates."

## Problem
Two users purchasing the last item simultaneously can both read stock = 1 and both successfully purchase, overselling inventory.

## Prediction
Database isolation levels (Read Committed, Repeatable Read, Serializable) control visibility and concurrency anomalies.

## Why this matters
Understanding isolation prevents subtle financial bugs that only appear under concurrent production load.

## First principles
SQL-92 Isolation Levels: Read Uncommitted, Read Committed (PostgreSQL default), Repeatable Read, Serializable.

## Mental model
```text
Request A: Read Stock (1) ──┐ (Race Condition) ──> Overwrites with 0
Request B: Read Stock (1) ──┴──> Overwrites with 0  --> Stock oversold to -1!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Row-level locking (`SELECT ... FOR UPDATE`) preventing concurrent read-modify-write races.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/25-isolation-and-concurrent-requests/tests/ -v
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
- **Failure Injection**: Run concurrent updates without locking; observe final stock balance drops below zero (lost update anomaly).
- Execute the experiment script:
```bash
python phases/25-isolation-and-concurrent-requests/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect transaction logs; identify concurrent read of uncommitted or stale state.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Apply pessimistic locking (`SELECT FOR UPDATE`) or atomic SQL expressions (`UPDATE items SET stock = stock - 1 WHERE stock >= 1`).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Pessimistic row locks can cause database deadlocks if multiple rows are acquired in differing orders across transactions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: PostgreSQL uses Multi-Version Concurrency Control (MVCC) so readers never block writers and writers never block readers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a Lost Update anomaly and how does concurrent traffic trigger it?
2. How does SELECT FOR UPDATE prevent two transactions from simultaneously reading the same row?
3. Why does PostgreSQL use Read Committed as its default isolation level instead of Serializable?

## What comes next
Having understood isolation and concurrent requests, we next discover its inherent boundaries and transition to **Optimistic Concurrency**.
