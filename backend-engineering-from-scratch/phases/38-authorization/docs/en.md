# Lesson 38: Authorization

> **Motto**: Authorization determines whether an authenticated principal has permission to perform an action on a specific resource.

---

## Motto
"Authorization determines whether an authenticated principal has permission to perform an action on a specific resource."

## Problem
Checking authentication without authorization allows any logged-in user to view or delete any other user's data.

## Prediction
Enforcing authorization policies at the application boundary protects data confidentiality and integrity.

## Why this matters
Authorization bugs (BOLA / IDOR) are consistently ranked as the #1 critical API security vulnerability.

## First principles
Decision = Evaluate(Principal, Action, Resource, Context). Result is ALLOW or DENY.

## Mental model
```text
Authenticated User -> AuthZ Policy Engine -> Check (User.id, 'DELETE', Order.id) -> ALLOW / 403 Forbidden
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI Security dependencies and permission decorators.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/38-authorization/tests/ -v
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
- **Failure Injection**: User A attempts to access or modify a resource owned exclusively by User B.
- Execute the experiment script:
```bash
python phases/38-authorization/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Policy engine detects unauthorized resource access and returns HTTP 403 Forbidden.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce authorization checks in the application service layer, not solely in route controllers.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Broken Object-Level Authorization (BOLA/IDOR): changing `/orders/100` to `/orders/101` must not leak another user's order.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Log all authorization denials with user ID, target resource, and IP address for security auditing.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between HTTP 401 Unauthorized and HTTP 403 Forbidden?
2. What is Broken Object-Level Authorization (BOLA) and why is it so prevalent?
3. Where in the application architecture should authorization rules be enforced?

## What comes next
Having understood authorization, we next discover its inherent boundaries and transition to **RBAC**.
