# Lesson 22: CRUD Correctly

> **Motto**: CRUD is not just INSERT and SELECT; it is the correct handling of missing entities, conflicts, and boundary invariants.

---

## Motto
"CRUD is not just INSERT and SELECT; it is the correct handling of missing entities, conflicts, and boundary invariants."

## Problem
Amateur CRUD implementations crash on missing IDs, corrupt data on partial updates, and ignore database constraints.

## Prediction
Implementing robust CRUD with proper status codes (404 on missing, 409 on conflict, 204 on delete) creates dependable APIs.

## Why this matters
CRUD operations are the foundation of business systems; getting them right prevents subtle data corruption.

## First principles
Create (201/409), Read (200/404), Update (200/404/409), Delete (204/404).

## Mental model
```text
Client Request -> Validate -> Check Existence -> Enforce Business Rule -> Execute SQL -> Handle DB Errors -> Return DTO
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI CRUD endpoints with Pydantic validation and error handling.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/22-crud-correctly/tests/ -v
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
- **Failure Injection**: Attempt to update a non-existent ID, insert a duplicate unique key, or delete an already deleted row.
- Execute the experiment script:
```bash
python phases/22-crud-correctly/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify correct HTTP status codes: 404 for missing, 409 for duplicate unique key, 204 for successful deletion.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Implement optimistic locking during update operations to prevent lost updates.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Authorization check must precede entity modification: verify caller ownership before update/delete.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Ensure soft-delete versus hard-delete requirements are explicitly documented and implemented.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should a DELETE request return 204 No Content instead of 200 OK with a message string?
2. How should an API handle a PUT request when the target resource ID does not exist?
3. What database error code indicates a UNIQUE constraint violation in PostgreSQL vs SQLite?

## What comes next
Having understood crud correctly, we next discover its inherent boundaries and transition to **Transactions**.
