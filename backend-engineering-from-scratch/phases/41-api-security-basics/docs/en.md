# Lesson 41: API Security Basics

> **Motto**: API security requires defense-in-depth: boundary validation, authentication, least privilege, rate limiting, and safe headers.

---

## Motto
"API security requires defense-in-depth: boundary validation, authentication, least privilege, rate limiting, and safe headers."

## Problem
Securing an API by relying on a single defensive layer (e.g. firewall) guarantees catastrophic failure when that layer is breached.

## Prediction
Layering input sanitization, cryptographic auth, strict CORS, and rate limiting protects against multi-vector attacks.

## Why this matters
Understanding the OWASP API Security Top 10 transforms security from a vague anxiety into concrete engineering controls.

## First principles
Security is an unbroken chain of defensive invariants at every layer of the system.

## Mental model
```text
Ingress Firewall -> Rate Limiter -> TLS/CORS -> AuthN -> Schema Validation -> AuthZ -> Parameterized SQL
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI security middleware and CORS configurations.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/41-api-security-basics/tests/ -v
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
- **Failure Injection**: Send an oversized 100MB payload or an origin header from an untrusted domain.
- Execute the experiment script:
```bash
python phases/41-api-security-basics/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Security middleware rejects payload with 413 Payload Too Large and blocks untrusted CORS preflight.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Inject standard security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Strict-Transport-Security`.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Security through obscurity is an anti-pattern: hiding endpoint URLs does not substitute for authentication.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Regular automated vulnerability scanning and dependency audits are mandatory for production releases.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the top 3 vulnerabilities in the OWASP API Security Top 10?
2. Why is defense-in-depth essential in modern distributed cloud architectures?
3. What attack is mitigated by the `X-Content-Type-Options: nosniff` header?

## What comes next
Having understood api security basics, we next discover its inherent boundaries and transition to **SQL Injection**.
