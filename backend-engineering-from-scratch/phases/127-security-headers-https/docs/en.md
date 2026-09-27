# Lesson 127: Security Headers / HTTPS

> **Motto**: Security headers instruct browsers to enforce strict transport security, prevent MIME confusion, and block clickjacking.

---

## Motto
"Security headers instruct browsers to enforce strict transport security, prevent MIME confusion, and block clickjacking."

## Problem
Omitting security headers leaves web clients vulnerable to Man-In-The-Middle attacks, clickjacking, and XSS injection.

## Prediction
Configuring HSTS, CSP, X-Frame-Options, and X-Content-Type-Options hardens the HTTP response perimeter.

## Why this matters
Security headers provide simple, zero-cost defense-in-depth against common client-side web attacks.

## First principles
Headers: Strict-Transport-Security (Force HTTPS) + Content-Security-Policy (XSS defense) + X-Frame-Options (Clickjacking defense).

## Mental model
```text
Server Response Headers ──[HSTS + CSP + X-Frame-Options: DENY]──> Browser enforces strict security perimeter
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI security header middleware configurations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/127-security-headers-https/tests/ -v
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
- **Failure Injection**: Query the API using cURL; inspect response headers; verify HSTS, CSP, and X-Content-Type-Options are present.
- Execute the experiment script:
```bash
python phases/127-security-headers-https/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Attempt to render the API in an iframe; observe browser blocks execution due to `X-Frame-Options: DENY`.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce HSTS with `max-age=31536000; includeSubDomains; preload` once HTTPS is verified across all subdomains.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never transmit API credentials or cookies over unencrypted plaintext HTTP; always redirect HTTP to HTTPS.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Audit security headers regularly using automated scanners like Mozilla Observatory.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What does the HTTP Strict Transport Security (HSTS) header instruct browsers to do?
2. How does the `X-Content-Type-Options: nosniff` header prevent MIME confusion attacks?
3. What attack vector is mitigated by configuring `X-Frame-Options: DENY`?

## What comes next
Having understood security headers / https, we next discover its inherent boundaries and transition to **Dependency Security**.
