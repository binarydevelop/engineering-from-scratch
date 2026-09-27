# Lesson 44: CSRF

> **Motto**: Cross-Site Request Forgery tricks an authenticated browser into submitting unauthorized requests to a trusted application.

---

## Motto
"Cross-Site Request Forgery tricks an authenticated browser into submitting unauthorized requests to a trusted application."

## Problem
Using cookie-based authentication without CSRF defenses allows rogue websites to execute bank transfers on behalf of victims.

## Prediction
Implementing anti-forgery tokens (Double Submit Cookie or Synchronizer Token) guarantees request origin authenticity.

## Why this matters
Bearer token APIs using `Authorization` headers are immune to CSRF, but cookie-based backends require strict defense.

## First principles
Attacker site causes browser to send request to target.com -> Browser automatically attaches target.com cookies -> CSRF!

## Mental model
```text
Legitimate Form includes Secret CSRF Token -> Server validates Token matches Cookie Token -> Rejects requests missing Token
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI CSRF middleware protecting cookie-authenticated endpoints.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/44-csrf/tests/ -v
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
- **Failure Injection**: Submit a mutating POST request with valid session cookies but missing the CSRF anti-forgery header.
- Execute the experiment script:
```bash
python phases/44-csrf/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Server catches missing CSRF token and rejects request with HTTP 403 Forbidden.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Combine `SameSite=Lax` or `SameSite=Strict` on session cookies with explicit anti-CSRF token verification.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: JSON endpoints accepting `Content-Type: application/json` provide partial CSRF protection because browsers require preflight.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Modern web backends prefer Bearer tokens in headers for APIs, completely eliminating CSRF attack surfaces.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Cross-Site Request Forgery (CSRF) exploit browser cookie behavior?
2. Why are APIs using `Authorization: Bearer <token>` headers immune to CSRF attacks?
3. How does the Double Submit Cookie pattern protect against CSRF?

## What comes next
Having understood csrf, we next discover its inherent boundaries and transition to **Rate Limiting From Scratch**.
