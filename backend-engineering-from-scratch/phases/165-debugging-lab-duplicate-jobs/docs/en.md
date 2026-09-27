# Lesson 165: Debugging Lab: Duplicate Jobs

> **Motto**: Diagnosing duplicate side effects (double billing, duplicate emails) requires identifying non-idempotent worker task retries.

---

## Motto
"Diagnosing duplicate side effects (double billing, duplicate emails) requires identifying non-idempotent worker task retries."

## Problem
A customer is charged twice for a single order because a worker timed out on the first attempt after charging and retried.

## Prediction
Adding database idempotency keys and state checks prevents duplicate task executions from repeating destructive side effects.

## Why this matters
Eliminating duplicate job side effects is mandatory for financial accuracy and reliable asynchronous processing.

## First principles
Worker 1 charges card -> Network drops before ACK -> Queue re-delivers job -> Worker 2 charges card AGAIN! (Double Charge!)

## Mental model
```text
Remedy: Check unique `idempotency_key` in DB -> If exists, skip charge -> Prevents duplicate financial side effects!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Worker deduplication patterns and idempotency tables.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/165-debugging-lab-duplicate-jobs/tests/ -v
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
- **Failure Injection**: Simulate a worker task that times out and re-executes; observe duplicate billing record created in un-defended code.
- Execute the experiment script:
```bash
python phases/165-debugging-lab-duplicate-jobs/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Implement unique transaction idempotency key check; re-run test; assert exactly one charge occurs despite multiple executions.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never assume a message queue will deliver a task exactly once: in distributed networks, delivery is always *at-least-once*.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Idempotency must be enforced at the ground truth storage layer using database UNIQUE constraints.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Log duplicate task detection events to verify how often distributed at-least-once delivery triggers in production.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is 'exactly-once delivery' mathematically impossible across fallible distributed networks?
2. How does a database UNIQUE constraint on an idempotency key prevent duplicate billing executions?
3. What should a background worker do when it discovers a task with an already-processed idempotency key?

## What comes next
Having understood debugging lab: duplicate jobs, we next discover its inherent boundaries and transition to **Debugging Lab: Stale Cache**.
