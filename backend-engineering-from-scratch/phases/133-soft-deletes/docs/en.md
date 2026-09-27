# Lesson 133: Soft Deletes

> **Motto**: Soft deletes mark database records as inactive via a timestamp (`deleted_at`) rather than physically removing rows from disk.

---

## Motto
"Soft deletes mark database records as inactive via a timestamp (`deleted_at`) rather than physically removing rows from disk."

## Problem
Accidentally deleting customer data with raw `DELETE` statements makes accidental data recovery impossible without restoring backups.

## Prediction
Setting `deleted_at = NOW()` preserves audit history and enables undo features, but complicates queries and unique constraints.

## Why this matters
Understanding soft delete tradeoffs prevents query bugs where deleted records accidentally appear in search results.

## First principles
Hard Delete: `DELETE FROM users WHERE id = 1` (Gone). Soft Delete: `UPDATE users SET deleted_at = NOW() WHERE id = 1`.

## Mental model
```text
Active Query: `SELECT * FROM items WHERE deleted_at IS NULL` -> Excludes soft-deleted records from standard views
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: SQLAlchemy custom query filters and soft delete mixins.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/133-soft-deletes/tests/ -v
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
- **Failure Injection**: Soft-delete an entity; query all active entities; verify soft-deleted entity is excluded from standard list queries.
- Execute the experiment script:
```bash
python phases/133-soft-deletes/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Execute an administrative restore operation (`SET deleted_at = NULL`); verify entity reappears in active queries.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Unique index hazard: `UNIQUE (email)` fails when a soft-deleted user tries to re-register. Fix: Partial index `WHERE deleted_at IS NULL`.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Soft-deleted data is still subject to GDPR 'Right to be Forgotten'; compliance may mandate permanent hard deletion upon request.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Soft deletes cause table bloat over time; archive old soft-deleted records to cold storage to maintain query performance.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the operational advantages and disadvantages of soft deletes versus hard deletes?
2. How does a soft delete break a standard database UNIQUE constraint on an email column?
3. What is a PostgreSQL partial index and how does it solve unique constraints on soft-deleted tables?

## What comes next
Having understood soft deletes, we next discover its inherent boundaries and transition to **Audit History**.
