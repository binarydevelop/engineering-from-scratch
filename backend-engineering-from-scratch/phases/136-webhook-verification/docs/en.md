# Lesson 136: Webhook Verification

> **Motto**: Webhook verification allows receivers to cryptographically verify that an incoming webhook was sent by the authentic provider.

---

## Motto
"Webhook verification allows receivers to cryptographically verify that an incoming webhook was sent by the authentic provider."

## Problem
Accepting webhooks without verification allows attackers to spoof payment notifications and mark orders as paid for free.

## Prediction
Signing webhook payloads with HMAC-SHA256 and including timestamps prevents payload tampering and replay attacks.

## Why this matters
Cryptographic webhook verification is mandatory for secure financial and integration architectures.

## First principles
Provider signs: `Signature = HMAC-SHA256(Secret, Timestamp + '.' + Body)`. Header: `X-Signature: t=123,v1=hex`.

## Mental model
```text
Provider: Signs (Secret + Payload) -> Sends Signature Header -> Receiver: Computes HMAC -> Compares -> Verified!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Stripe / GitHub webhook verification pattern in FastAPI endpoints.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/136-webhook-verification/tests/ -v
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
- **Failure Injection**: Submit a webhook request with an invalid signature or altered payload body; verify receiver rejects with HTTP 401.
- Execute the experiment script:
```bash
python phases/136-webhook-verification/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Submit an authentic webhook with an expired timestamp (> 5 minutes old); verify receiver rejects replay attack.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use `hmac.compare_digest` for constant-time signature comparison to eliminate timing attack vulnerabilities.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Include the timestamp inside the signed payload to prevent replay attacks where an attacker re-sends valid captured requests.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Receivers must verify the raw, unparsed request bytes: JSON parsers can reorder keys, invalidating signatures.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does HMAC-SHA256 payload signing prove the authenticity and integrity of a webhook notification?
2. What is a webhook replay attack and how does signing a timestamp prevent it?
3. Why must webhook signature verification be performed on raw request bytes rather than parsed JSON dictionaries?

## What comes next
Having understood webhook verification, we next discover its inherent boundaries and transition to **External API Integration**.
