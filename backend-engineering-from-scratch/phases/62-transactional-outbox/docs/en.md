# Lesson 62: Transactional Outbox

> **Motto**: The Transactional Outbox pattern eliminates the dual-write problem by saving outbox events in the same database transaction.

---

## Motto
"The Transactional Outbox pattern eliminates the dual-write problem by saving outbox events in the same database transaction."

## Problem
Writing to a database and then publishing to an external message broker can fail midway, producing catastrophic inconsistency.

## Prediction
Inserting an event into an `outbox` table in the *same* SQL transaction guarantees at-least-once event delivery.

## Why this matters
The Transactional Outbox is the foundational pattern for reliable distributed data consistency without two-phase commit.

## First principles
Dual Write = Broken (DB commit succeeds, Broker publish fails -> Lost event). Outbox = Atomic SQL Transaction.

## Mental model
```text
BEGIN -> 1. INSERT INTO orders (...) -> 2. INSERT INTO outbox_events (...) -> COMMIT -> Asynchronous Relay reads & publishes
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Transactional Outbox pattern with PostgreSQL and message broker relay.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/62-transactional-outbox/tests/ -v
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
- **Failure Injection**: Simulate message broker crash immediately after database commit; observe that the outbox row preserves the event.
- Execute the experiment script:
```bash
python phases/62-transactional-outbox/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Restore broker; verify that the outbox relay discovers un-sent events, publishes them, and marks them as sent.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: The outbox relay guarantees *at-least-once* delivery; downstream consumers must be idempotent.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Purge or archive processed outbox events periodically to prevent the outbox table from growing infinitely.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Change Data Capture (CDC) tools like Debezium can read database WAL logs directly, eliminating polling overhead.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the Dual-Write problem and why can it not be solved with a simple try-except block?
2. How does writing events to an outbox table in the same ACID transaction guarantee event delivery?
3. Why does the Transactional Outbox pattern require downstream consumers to be idempotent?

## What comes next
Having understood transactional outbox, we next discover its inherent boundaries and transition to **Idempotency Keys**.
