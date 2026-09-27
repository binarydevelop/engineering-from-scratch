# Lesson 24: Transaction Boundaries

> **Motto**: A database transaction must span exactly one business consistency boundary; wrapping entire HTTP requests in transactions is fatal.

---

## Motto
"A database transaction must span exactly one business consistency boundary; wrapping entire HTTP requests in transactions is fatal."

## Problem
Opening a database transaction at the start of an HTTP request holds locks during slow JSON serialization and network I/O.

## Prediction
Scoping transactions tightly around necessary SQL mutations maximizes throughput and prevents catastrophic lock contention.

## Why this matters
Poor transaction boundaries cause cascading lock timeouts, deadlocks, and connection pool starvation.

## First principles
A transaction boundary should encapsulate only the operations that require strict atomic consistency.

## Mental model
```text
Request Arrives -> Validate & Authorize (No Tx) -> Service Begins Tx -> Execute SQL Writes -> Commit Tx -> Network I/O (No Tx)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Scoped transaction decorators and context managers in application services.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/24-transaction-boundaries/tests/ -v
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
- **Failure Injection**: Simulate a slow 2-second external API call inside an active database transaction under 50 concurrent requests.
- Execute the experiment script:
```bash
python phases/24-transaction-boundaries/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe database connection pool completely exhausted and all other endpoints blocked waiting for locks.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Refactor: move external network calls and heavy serialization completely outside the transaction block.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Holding database transactions open during untrusted client network uploads allows trivial Denial of Service attacks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Transaction duration is a primary database health metric; p99 transaction time should be under 50ms.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is wrapping an entire HTTP request in a database transaction an operational anti-pattern?
2. What happens to database locks when a transaction is held open during a 3-second external API call?
3. How do you determine the minimum necessary boundary for an ACID transaction?

## What comes next
Having understood transaction boundaries, we next discover its inherent boundaries and transition to **Isolation and Concurrent Requests**.
