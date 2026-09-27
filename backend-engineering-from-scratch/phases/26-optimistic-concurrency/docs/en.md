# Lesson 26: Optimistic Concurrency

> **Motto**: Optimistic concurrency control uses version numbers to detect and reject conflicting concurrent updates without holding locks.

---

## Motto
"Optimistic concurrency control uses version numbers to detect and reject conflicting concurrent updates without holding locks."

## Problem
Pessimistic locking holds database locks for extended periods, reducing concurrency and risking deadlocks.

## Prediction
Checking a version column on update (`WHERE id = :id AND version = :expected_version`) guarantees collision detection.

## Why this matters
Optimistic locking allows high read throughput while guaranteeing that concurrent edits never silently overwrite each other.

## First principles
Assume conflicts are rare: read without locking; upon write, verify that state has not changed since read.

## Mental model
```text
Read Entity (Version 1) -> User Edits -> UPDATE ... SET version = 2 WHERE id = :id AND version = 1 -> Rows Affected: 1 (Success) | 0 (Conflict!)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SQLAlchemy version_id_col and application-level version checking.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/26-optimistic-concurrency/tests/ -v
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
- **Failure Injection**: Two concurrent clients read Version 1 and attempt to submit updates simultaneously.
- Execute the experiment script:
```bash
python phases/26-optimistic-concurrency/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: First update increments version to 2; second update matches 0 rows and returns HTTP 409 Conflict.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Provide client with the updated version and allow user reconciliation or automated retry.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Optimistic locking prevents the classic 'Last Write Wins' data loss bug in multi-user web applications.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: If update collision rate exceeds 20%, optimistic locking retry storms can degrade performance; consider pessimistic locks.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does a conditional UPDATE query detect that another transaction modified a row?
2. What HTTP status code should an API return when an optimistic lock collision occurs?
3. When is optimistic concurrency preferred over pessimistic row locking?

## What comes next
Having understood optimistic concurrency, we next discover its inherent boundaries and transition to **Database Constraints as Defense**.
