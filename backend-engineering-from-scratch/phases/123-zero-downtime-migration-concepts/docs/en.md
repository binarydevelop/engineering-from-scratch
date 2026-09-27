# Lesson 123: Zero-Downtime Migration Concepts

> **Motto**: Zero-downtime migrations use the Expand-Contract (Parallel Run) pattern to evolve schemas safely across multiple deployments.

---

## Motto
"Zero-downtime migrations use the Expand-Contract (Parallel Run) pattern to evolve schemas safely across multiple deployments."

## Problem
Directly renaming a column requires stopping the application, migrating the database, and restarting, causing downtime.

## Prediction
The Expand-Contract pattern splits schema changes into 4 phased releases: Expand, Dual-Write, Backfill, and Contract.

## Why this matters
Expand-Contract enables non-disruptive column renames, type changes, and table splits on massive production databases.

## First principles
Phase 1: Add new column (Expand) -> Phase 2: Write to both columns -> Phase 3: Backfill historical data -> Phase 4: Drop old column (Contract).

## Mental model
```text
Release 1 (Expand): ADD col_new -> Release 2: Code writes to col_old AND col_new -> Release 3: Code reads col_new -> Release 4: DROP col_old
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Phased Alembic migrations and application model transitions.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/123-zero-downtime-migration-concepts/tests/ -v
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
- **Failure Injection**: Execute continuous read/write load against a service while performing the 4-phase Expand-Contract migration.
- Execute the experiment script:
```bash
python phases/123-zero-downtime-migration-concepts/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify zero 500 errors and 100% data consistency throughout all four deployment transitions.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Backfills of historical data should be executed in small, paced batches (e.g. 1,000 rows at a time) to prevent table locks.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never run all 4 phases in a single deployment: each phase must be deployed, verified, and stabilized independently.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Zero-downtime migration discipline separates novice developers from senior production engineers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the four distinct phases of the Expand-Contract (Parallel Run) database migration pattern?
2. Why must historical data backfills be performed in small batches rather than a single giant UPDATE statement?
3. How does the Expand-Contract pattern eliminate customer-facing downtime during schema evolutions?

## What comes next
Having understood zero-downtime migration concepts, we next discover its inherent boundaries and transition to **CI Basics**.
