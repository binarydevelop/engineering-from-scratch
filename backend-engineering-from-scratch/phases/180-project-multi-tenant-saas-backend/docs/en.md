# Lesson 180: Project: Multi-Tenant SaaS Backend

> **Motto**: Build a production multi-tenant SaaS backend with strict organizational tenant isolation, RBAC membership, and audit logging.

---

## Motto
"Build a production multi-tenant SaaS backend with strict organizational tenant isolation, RBAC membership, and audit logging."

## Problem
A multi-tenant backend with weak isolation risks leaking private enterprise data to competitor organizations, causing fatal legal breaches.

## Prediction
Enforcing tenant scoping on every query, role-based memberships (Owner, Admin, Member), and audit trails guarantees isolation.

## Why this matters
Multi-tenancy is the core architecture powering B2B SaaS platforms (Slack, Notion, GitHub).

## First principles
User belongs to Organization. All tables have `tenant_id`. Every query filtered: `WHERE tenant_id = :tenant_id`.

## Mental model
```text
User Token (Tenant: org_123) -> Middleware injects Tenant Context -> SQL queries strictly scoped to `tenant_id = 'org_123'`
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: B2B Multi-tenant SaaS architecture reference.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/180-project-multi-tenant-saas-backend/tests/ -v
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
- **Failure Injection**: Simulate User in Org A attempting to access documents belonging to Org B; verify complete query isolation.
- Execute the experiment script:
```bash
python phases/180-project-multi-tenant-saas-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify user can switch active organizations and permissions dynamically; verify all tenant mutations are recorded in audit logs.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce uniqueness constraints within tenant scopes: `UNIQUE (tenant_id, document_name)` allows duplicate names across orgs.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Combine application query scoping with PostgreSQL Row-Level Security (RLS) as a defense-in-depth security layer.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Never trust client-supplied tenant IDs in URLs without verifying that the authenticated user belongs to that tenant.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Row-Level Multi-Tenancy differ from Schema-per-Tenant or Database-per-Tenant architectures?
2. Why must database unique constraints in multi-tenant systems always include the `tenant_id` column?
3. How do you prevent Insecure Direct Object References (IDOR) across different organizational tenants?

## What comes next
Having understood project: multi-tenant saas backend, we next discover its inherent boundaries and transition to **Project: Real-Time Chat Backend**.
