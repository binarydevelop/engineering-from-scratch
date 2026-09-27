# Lesson 40: Resource-Based Authorization

> **Motto**: Resource-based authorization evaluates permissions in the context of the specific target entity and its relationship to the caller.

---

## Motto
"Resource-based authorization evaluates permissions in the context of the specific target entity and its relationship to the caller."

## Problem
Relying solely on roles allows any 'user' to edit any other user's profile or read their invoices.

## Prediction
Validating relationships (Owner, Collaborator, Org Member) against the specific database record guarantees tenant isolation.

## Why this matters
Resource authorization closes IDOR vulnerabilities and enforces true multi-tenant data boundaries.

## First principles
Allow = Caller.id == Resource.owner_id OR Caller.id IN Resource.collaborators OR Caller.is_admin.

## Mental model
```text
Request (Edit Document 42) -> Fetch Document 42 -> Check: Is Caller the Owner or Collaborator? -> Allow / 403
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI dependencies fetching target resources and verifying caller relationship before handler execution.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/40-resource-based-authorization/tests/ -v
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
- **Failure Injection**: Attacker crafts a request updating a document ID belonging to a different tenant/user.
- Execute the experiment script:
```bash
python phases/40-resource-based-authorization/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Checker verifies document.owner_id != caller.id and aborts with HTTP 403 Forbidden.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Incorporate ownership checks directly into SQL queries: `WHERE id = :id AND owner_id = :caller_id`.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: IDOR: Never assume an authenticated user has permission to interact with an arbitrary resource ID.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Returning 404 instead of 403 for unauthorized resources prevents enumeration of resource IDs by attackers.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Resource-Based Authorization prevent Insecure Direct Object References (IDOR)?
2. Why do security-conscious APIs return HTTP 404 instead of 403 when a user lacks access to a resource?
3. How can ownership verification be embedded directly into database SQL queries?

## What comes next
Having understood resource-based authorization, we next discover its inherent boundaries and transition to **API Security Basics**.
