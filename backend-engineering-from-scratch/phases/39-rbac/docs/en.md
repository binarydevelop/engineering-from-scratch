# Lesson 39: RBAC

> **Motto**: Role-Based Access Control assigns permissions to roles, and roles to users, simplifying coarse access management.

---

## Motto
"Role-Based Access Control assigns permissions to roles, and roles to users, simplifying coarse access management."

## Problem
Hardcoding permission checks like `if user.role == 'admin'` across dozens of endpoints creates brittle authorization.

## Prediction
Mapping users to roles (Admin, Editor, Viewer) and roles to fine-grained permission sets scales permissions cleanly.

## Why this matters
RBAC centralizes access governance, making onboarding and permission audits straightforward.

## First principles
User -> Assigned Roles -> Role contains Permissions -> Endpoint requires Permission.

## Mental model
```text
User (Alice) -> Role (Editor) -> Permissions ('posts:create', 'posts:edit') -> Endpoint ('posts:delete' DENIED)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Role-checking dependencies in FastAPI route decorators.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/39-rbac/tests/ -v
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
- **Failure Injection**: A user with 'Viewer' role attempts to trigger a POST mutation requiring 'Editor' role.
- Execute the experiment script:
```bash
python phases/39-rbac/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: RBAC validator asserts missing permission and returns HTTP 403 Forbidden.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Separate roles from permissions: check permissions on endpoints (`has_permission('orders:cancel')`), not role names.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Role explosion: as organizations grow, creating specialized roles for every variation becomes unmanageable.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: RBAC fails to address object ownership (e.g. can an Editor edit *any* post, or only their own?); resource auth is needed.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is checking for fine-grained permissions better than checking role names directly in handlers?
2. What is 'role explosion' in enterprise RBAC systems?
3. What is the fundamental limitation of RBAC when handling resource ownership?

## What comes next
Having understood rbac, we next discover its inherent boundaries and transition to **Resource-Based Authorization**.
