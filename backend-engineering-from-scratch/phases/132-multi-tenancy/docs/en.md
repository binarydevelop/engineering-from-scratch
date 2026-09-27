# Lesson 132: Multi-Tenancy

> **Motto**: Multi-tenancy serves multiple independent customer organizations from a shared backend while guaranteeing strict data isolation.

---

## Motto
"Multi-tenancy serves multiple independent customer organizations from a shared backend while guaranteeing strict data isolation."

## Problem
A single missing `WHERE tenant_id = :tenant_id` clause in a database query leaks private corporate data to another customer.

## Prediction
Enforcing tenant scoping at the authentication, repository, and database level prevents catastrophic cross-tenant data leaks.

## Why this matters
Tenant isolation is the core engineering contract of Software-as-a-Service (SaaS) backend platforms.

## First principles
Tenant Models: Shared Database / Shared Schema (Row-Level `tenant_id`), Separate Schema, or Separate Database.

## Mental model
```text
Request -> Extract tenant_id from Verified Token -> Repository forces `WHERE tenant_id = :tenant_id` on ALL queries!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI tenant resolution dependencies and scoped database sessions.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/132-multi-tenancy/tests/ -v
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
- **Failure Injection**: Simulate Tenant A attempting to read an order belonging to Tenant B by guessing the primary key ID.
- Execute the experiment script:
```bash
python phases/132-multi-tenancy/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Repository enforces tenant scoping; query returns 0 rows; endpoint safely returns HTTP 404 Not Found.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Combine application-level tenant scoping with PostgreSQL Row-Level Security (RLS) for defense-in-depth.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Ensure unique constraints include the tenant ID: `UNIQUE (tenant_id, sku)` allows different tenants to use the same SKU.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Never accept `tenant_id` as an untrusted query parameter; always resolve tenant identity from the verified authentication token.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the three common database architectural models for multi-tenant SaaS applications?
2. How does Row-Level Security (RLS) in PostgreSQL enforce tenant isolation at the database engine level?
3. Why must tenant identity always be resolved from verified authentication tokens rather than request query parameters?

## What comes next
Having understood multi-tenancy, we next discover its inherent boundaries and transition to **Soft Deletes**.
