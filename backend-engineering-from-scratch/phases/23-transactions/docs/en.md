# Lesson 23: Transactions

> **Motto**: An ACID transaction groups multiple database operations into an atomic unit that either completely succeeds or leaves no trace.

---

## Motto
"An ACID transaction groups multiple database operations into an atomic unit that either completely succeeds or leaves no trace."

## Problem
When a multi-step operation fails midway (e.g. money deducted but order insertion fails), state becomes corrupted.

## Prediction
Wrapping multi-step mutations in BEGIN and COMMIT guarantees atomicity and consistency even during crashes.

## Why this matters
Without transactions, power loss, process crashes, or network failures create irrecoverable financial and data corruption.

## First principles
ACID: Atomicity (all-or-nothing), Consistency (rules hold), Isolation (no cross-talk), Durability (written to disk).

## Mental model
```text
BEGIN -> 1. Deduct Inventory -> 2. Charge Account (FAILS) -> ROLLBACK -> State Restored to Exact Pre-Transaction State
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Database transaction context managers (`with db.transaction():`) in Python drivers.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/23-transactions/tests/ -v
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
- **Failure Injection**: Inject an exception or simulated crash between step 1 and step 2 of a multi-table mutation.
- Execute the experiment script:
```bash
python phases/23-transactions/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inspect database tables; confirm that step 1 was completely rolled back and no partial data remains.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep transactions as short as humanly possible to minimize row lock contention.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Transactions do not protect against bugs outside the database; external API calls must NOT run inside DB transactions.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Long-running transactions hold database locks, causing lock queues and connection pool exhaustion.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What happens to uncommitted database changes when a backend process crashes?
2. Why must an outbound HTTP call to a payment gateway never run inside a database transaction block?
3. What is the difference between database rollback and application-level compensation?

## What comes next
Having understood transactions, we next discover its inherent boundaries and transition to **Transaction Boundaries**.
