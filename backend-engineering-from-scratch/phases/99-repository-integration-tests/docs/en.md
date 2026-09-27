# Lesson 99: Repository Integration Tests

> **Motto**: Repository integration tests verify SQL queries, transactions, and constraints against a real database engine.

---

## Motto
"Repository integration tests verify SQL queries, transactions, and constraints against a real database engine."

## Problem
Mocking the database in repository tests hides SQL syntax errors, broken JOINs, and constraint violations.

## Prediction
Executing repository methods against real SQLite or PostgreSQL databases validates query correctness and data mapping.

## Why this matters
Integration tests are the only reliable way to verify that complex SQL queries and migrations actually work.

## First principles
Test -> Repository -> Database Connection -> Real SQL Engine -> Assert Row Inserted & Constraints Enforced.

## Mental model
```text
Test Repository.save(order) -> Real SQL INSERT -> Verify Row Exists -> Attempt Duplicate -> Assert UniqueViolation
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pytest database fixtures managing schema creation, rollback transactions, and teardown.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/99-repository-integration-tests/tests/ -v
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
- **Failure Injection**: Attempt to insert a row violating a foreign key constraint against the real test database.
- Execute the experiment script:
```bash
python phases/99-repository-integration-tests/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert that the real database raises an integrity violation error; confirm repository handles error cleanly.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use transactional rollbacks per test: wrap each test in a transaction and roll back on teardown for instant test resets.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never run integration tests against shared staging or production databases; use dedicated local test instances.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Test database migrations against the real database engine during integration test setup.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is mocking the database in repository tests considered a dangerous anti-pattern?
2. How does wrapping individual integration tests in transactional rollbacks keep tests fast and isolated?
3. What database-specific behaviors can ONLY be tested against a real database engine?

## What comes next
Having understood repository integration tests, we next discover its inherent boundaries and transition to **API Tests**.
