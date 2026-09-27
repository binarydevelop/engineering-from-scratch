# Lesson 30: Database Migrations

> **Motto**: Database migrations are ordered, version-controlled scripts that evolve database schemas consistently across environments.

---

## Motto
"Database migrations are ordered, version-controlled scripts that evolve database schemas consistently across environments."

## Problem
Manually altering database tables in production causes schema drift, failed deployments, and data loss.

## Prediction
Tracking schema changes as versioned migration files guarantees that local, staging, and production databases match.

## Why this matters
Migrations make schema evolution repeatable, testable in CI pipelines, and auditable in version control.

## First principles
Schema Version N -> Migration Step (Up / Down) -> Schema Version N+1 with recorded migration metadata table.

## Mental model
```text
Migration File (Timestamp + SQL DDL) -> Migration Runner -> Execute DDL -> Update schema_migrations Table
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Alembic migration tool integrated with SQLAlchemy models.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/30-database-migrations/tests/ -v
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
- **Failure Injection**: Attempt to run a migration that contains an invalid SQL syntax error midway.
- Execute the experiment script:
```bash
python phases/30-database-migrations/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Migration runner catches error, aborts, and ensures schema version table is not incremented.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Wrap DDL migrations in transactions where the database engine supports transactional DDL (PostgreSQL).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never store plaintext passwords or seed test data with production credentials inside migration scripts.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Table-locking DDL operations (e.g. `ADD COLUMN DEFAULT` on older databases) can lock production tables for hours.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must database schema changes be version-controlled in the same repository as application code?
2. What is transactional DDL and which relational database engines support it?
3. How does the schema migrations tracking table prevent applying the same migration twice?

## What comes next
Having understood database migrations, we next discover its inherent boundaries and transition to **Pagination**.
