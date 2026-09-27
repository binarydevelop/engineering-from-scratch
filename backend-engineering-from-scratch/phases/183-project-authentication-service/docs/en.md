# Lesson 183: Project: Authentication Service

> **Motto**: Build a complete security authentication microservice with bcrypt registration, JWT issuance, refresh token rotation, and RBAC.

---

## Motto
"Build a complete security authentication microservice with bcrypt registration, JWT issuance, refresh token rotation, and RBAC."

## Problem
Flawed authentication architectures store passwords in plaintext, omit token expiration, or fail to rotate refresh tokens.

## Prediction
Implementing salted bcrypt hashing, short-lived JWT access tokens, refresh token rotation, and password reset flows ensures security.

## Why this matters
Authentication services protect user identities and serve as the single source of security truth for backend architectures.

## First principles
POST /register (bcrypt hash) -> POST /login (issues Access Token 15m + Refresh Token 7d) -> POST /refresh (rotates tokens).

## Mental model
```text
Client -> Login -> Receives Access Token (15m) + Refresh Token (7d) -> Access expires -> Refresh Token Rotated -> New Tokens Issued
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Authentication and identity microservice implementation.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/183-project-authentication-service/tests/ -v
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
- **Failure Injection**: Register a user, log in, access protected endpoint with JWT, let access token expire, refresh tokens successfully.
- Execute the experiment script:
```bash
python phases/183-project-authentication-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Attempt to reuse an already-used refresh token; observe token reuse detection triggers immediate revocation of all family tokens.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce Refresh Token Rotation: every refresh token can only be used once; issuing a new pair revokes the previous refresh token.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Token Reuse Detection: if a stolen refresh token is used after rotation, immediately revoke all tokens for that user session.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Follow current conservative security guidance: bcrypt work factor >= 12; JWT signed with HS256/RS256; enforce `exp` claim.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should JWT access tokens have short lifetimes (e.g. 15 minutes) paired with longer-lived refresh tokens?
2. What is Refresh Token Rotation and how does Token Family Reuse Detection stop credential theft?
3. Why must passwords be hashed using salted, adaptive work-factor algorithms rather than general-purpose hash functions?

## What comes next
Having understood project: authentication service, we next discover its inherent boundaries and transition to **Capstone 1: Production-Grade Modular Monolith**.
