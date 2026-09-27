# Lesson 36: Session-Based Authentication

> **Motto**: Session authentication pairs an opaque cryptographic cookie with a stateful server-side session store.

---

## Motto
"Session authentication pairs an opaque cryptographic cookie with a stateful server-side session store."

## Problem
Storing sensitive user state inside unencrypted client cookies allows client tampering and privilege escalation.

## Prediction
Issuing random 32-byte session tokens stored in Redis or SQL gives the server instant revocation capability.

## Why this matters
Session revocation is immediate: deleting the session row in Redis instantly logs out the user across all devices.

## First principles
Client holds Opaque Token -> Server validates Token against Server Store -> Resolves User ID & Permissions.

## Mental model
```text
POST /login -> Server creates Session(id, user_id) -> Set-Cookie: session_id=abc; HttpOnly; Secure -> Client sends Cookie
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI session middleware using signed cookies and server-side storage.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/36-session-based-authentication/tests/ -v
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
- **Failure Injection**: Attempt to access protected endpoint after session has been deleted on the server.
- Execute the experiment script:
```bash
python phases/36-session-based-authentication/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Server fails session lookup and rejects request with HTTP 401, clearing client cookie.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Set `HttpOnly` (stops JavaScript theft), `Secure` (HTTPS only), and `SameSite=Lax` (stops CSRF) on cookies.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: XSS attacks can steal cookies unless `HttpOnly` is strictly enforced by the browser.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Stateful sessions require shared session stores (Redis) when scaling across multiple application replicas.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does `HttpOnly` protect session cookies against Cross-Site Scripting (XSS)?
2. What is the primary advantage of session-based authentication over stateless JWTs?
3. How does a multi-server backend share session state across replicas?

## What comes next
Having understood session-based authentication, we next discover its inherent boundaries and transition to **Token-Based Authentication**.
