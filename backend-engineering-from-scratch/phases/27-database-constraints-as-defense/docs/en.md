# Lesson 27: Database Constraints as Defense

> **Motto**: Application-level validation can race under concurrency; database constraints are the ultimate ground truth of integrity.

---

## Motto
"Application-level validation can race under concurrency; database constraints are the ultimate ground truth of integrity."

## Problem
Checking `if not user_exists(email): create_user(email)` in application code races when two requests arrive simultaneously.

## Prediction
Enforcing UNIQUE, FOREIGN KEY, CHECK, and NOT NULL constraints at the database engine stops invalid data permanently.

## Why this matters
Application code can have bugs or multiple replicas; database constraints guarantee data invariants regardless of caller.

## First principles
The database storage engine is the single point of truth where all concurrent write paths converge.

## Mental model
```text
App Check: Email free? (Yes) ──┐ (Concurrent Race) ──> DB UNIQUE Constraint: First commits, Second REJECTED!
App Check: Email free? (Yes) ──┘
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Database DDL defining PRIMARY KEY, UNIQUE, FOREIGN KEY, and CHECK constraints.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/27-database-constraints-as-defense/tests/ -v
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
- **Failure Injection**: Send two concurrent user registration requests with identical email addresses.
- Execute the experiment script:
```bash
python phases/27-database-constraints-as-defense/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Database raises UniqueViolation; application catches exception and returns HTTP 409 Conflict.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Handle database constraint exceptions gracefully in the repository layer and map to domain conflicts.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Without database constraints, malicious or buggy clients can corrupt referential integrity and orphan financial records.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Adding constraints to large production tables requires careful indexing and lock management to avoid downtime.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does an application-level 'SELECT count(*) WHERE email = ...' check fail under concurrent traffic?
2. What is the difference between a CHECK constraint and an application schema validation rule?
3. How does a FOREIGN KEY constraint protect referential integrity during row deletion?

## What comes next
Having understood database constraints as defense, we next discover its inherent boundaries and transition to **ORM Introduction**.
