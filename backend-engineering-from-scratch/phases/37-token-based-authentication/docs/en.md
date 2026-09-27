# Lesson 37: Token-Based Authentication

> **Motto**: A signed JSON Web Token (JWT) allows stateless authentication by encoding cryptographically verified claims.

---

## Motto
"A signed JSON Web Token (JWT) allows stateless authentication by encoding cryptographically verified claims."

## Problem
Assuming a JWT is encrypted causes developers to store private passwords or secret keys inside token payloads.

## Prediction
JWTs are signed, not encrypted by default; any party can read the claims, but only the server with the key can sign.

## Why this matters
Stateless tokens eliminate database session lookups on every request, but make instant token revocation difficult.

## First principles
JWT = Base64(Header) . Base64(Claims) . HMAC-SHA256(Header.Claims, Secret).

## Mental model
```text
Client sends 'Authorization: Bearer <token>' -> Server verifies HMAC signature -> Extracts User Claims -> Authorizes Request
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: PyJWT integration in FastAPI OAuth2 password bearer dependencies.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/37-token-based-authentication/tests/ -v
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
- **Failure Injection**: Submit a token where the signature was stripped or claims payload was modified in transit.
- Execute the experiment script:
```bash
python phases/37-token-based-authentication/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Decoder detects signature mismatch or `alg: none` attack and raises InvalidSignatureError.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce short token lifetimes (e.g. 15 minutes) paired with refresh token rotation.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: The `alg: none` vulnerability allows attackers to forge tokens by specifying 'none' as the signature algorithm.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Revoking a stateless JWT before its `exp` time requires maintaining an active blocklist in Redis.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between a signed token (JWS) and an encrypted token (JWE)?
2. What happens if an API server fails to verify the signature of an incoming JWT?
3. Why is instant revocation difficult in a purely stateless JWT architecture?

## What comes next
Having understood token-based authentication, we next discover its inherent boundaries and transition to **Authorization**.
