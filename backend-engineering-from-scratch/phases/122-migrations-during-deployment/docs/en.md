# Lesson 122: Migrations During Deployment

> **Motto**: Database migrations must be sequenced carefully during rolling deployments to avoid breaking currently running application versions.

---

## Motto
"Database migrations must be sequenced carefully during rolling deployments to avoid breaking currently running application versions."

## Problem
Running a migration that renames a column while older application containers are still serving traffic causes instant 500 errors.

## Prediction
Sequencing migrations and ensuring backward-compatible schema changes allows rolling zero-downtime deployments.

## Why this matters
Understanding deployment and migration sequencing is critical for shipping updates without maintenance windows.

## First principles
Problem: Rolling update runs Old App and New App simultaneously. The database schema must satisfy BOTH simultaneously!

## Mental model
```text
Deploy Step 1: Run Backward-Compatible Migration -> Step 2: Rolling Deploy New App Containers -> Step 3: Cleanup Old Schema
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Alembic migration integration with CI/CD deployment pipelines.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/122-migrations-during-deployment/tests/ -v
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
- **Failure Injection**: Simulate a rolling deployment where Old App (v1) and New App (v2) run concurrently against a modified database schema.
- Execute the experiment script:
```bash
python phases/122-migrations-during-deployment/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that V1 continues serving requests without errors while V2 rolls out successfully.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Golden Rule of Database Deployment: Database changes must always be backward-compatible with the currently running code.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never run lock-heavy DDL (e.g. adding a NOT NULL column without a default on a 10M row table) during peak traffic.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Automate schema migrations as a pre-deployment step or release phase job before rolling out new application containers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does a rolling deployment require the database schema to support two different application versions simultaneously?
2. What happens if an application deployment executes `ALTER TABLE DROP COLUMN` while old containers are still active?
3. What is a Kubernetes pre-deployment Job and why is it used for database migrations?

## What comes next
Having understood migrations during deployment, we next discover its inherent boundaries and transition to **Zero-Downtime Migration Concepts**.
