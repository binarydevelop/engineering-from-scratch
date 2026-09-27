# Lesson 34: Authentication Problem

> **Motto**: Authentication establishes verified caller identity; it must remain strictly distinct from authorization.

---

## Motto
"Authentication establishes verified caller identity; it must remain strictly distinct from authorization."

## Problem
Conflating authentication (who you are) with authorization (what you can do) creates bypass vulnerabilities.

## Prediction
Establishing verified identities through credentials, sessions, or tokens enables access control.

## Why this matters
Authentication is the gatekeeper of all private data and state-modifying operations.

## First principles
Caller Identity (Principal) established via Proof of Secret (Password/Key) or Cryptographic Token.

## Mental model
```text
Credentials Submitted -> Verify Proof of Identity -> Issue Identity Token/Session -> Attach Principal to Request
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI security dependencies (`Security(get_current_user)`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/34-authentication-problem/tests/ -v
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
- **Failure Injection**: Send request with missing, expired, or forged credentials.
- Execute the experiment script:
```bash
python phases/34-authentication-problem/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that system immediately rejects with HTTP 401 Unauthorized and WWW-Authenticate header.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Establish clear user domain models with tenant ID, roles, and status.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Timing attacks: naive string comparison of passwords or tokens leaks execution timing; use hmac.compare_digest.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Authentication services must be heavily rate-limited to stop credential stuffing attacks.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the mechanical difference between authentication and authorization?
2. Why should an unauthenticated request return HTTP 401 instead of HTTP 403?
3. How does hmac.compare_digest prevent timing attack vulnerabilities?

## What comes next
Having understood authentication problem, we next discover its inherent boundaries and transition to **Password Storage**.
