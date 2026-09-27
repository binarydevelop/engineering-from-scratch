# Lesson 179: Project: Webhook Delivery Platform

> **Motto**: Build an enterprise webhook delivery system with subscriptions, HMAC signing, exponential backoff retries, and dead-letter queues.

---

## Motto
"Build an enterprise webhook delivery system with subscriptions, HMAC signing, exponential backoff retries, and dead-letter queues."

## Problem
Delivering webhooks naively fails when client receivers are down, slow, or timing out, blocking delivery queues.

## Prediction
Building durable delivery queues with HMAC-SHA256 signatures, backoff schedules, and dead-letter isolation ensures delivery at scale.

## Why this matters
Webhook platforms power integrations for payment processors (Stripe), developer tools (GitHub), and SaaS platforms.

## First principles
Event Triggered -> Match Subscriptions -> Queue Webhooks -> Worker signs with HMAC-SHA256 -> Delivers -> Retries with backoff.

## Mental model
```text
Event -> Webhook Engine -> Sign Payload (HMAC-SHA256) -> HTTP POST -> Success (ACK) | Failure -> Retry with Backoff -> DLQ
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Enterprise outbound webhook delivery platform.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/179-project-webhook-delivery-platform/tests/ -v
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
- **Failure Injection**: Register customer webhook endpoint; trigger 10 events; simulate customer server failing on first 2 attempts.
- Execute the experiment script:
```bash
python phases/179-project-webhook-delivery-platform/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify worker signs payloads, verifies delivery, retries failed attempts with backoff, and logs delivery history.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce strict connection timeouts (<= 5s) to prevent slow customer endpoints from tying up delivery worker threads.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Include `X-Webhook-Signature` and `X-Webhook-Timestamp` headers to enable customer verification and replay defense.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Automatically disable customer endpoints that fail continuously for more than 7 days to conserve infrastructure resources.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does HMAC-SHA256 payload signing allow webhook receivers to verify request authenticity?
2. What retry and backoff strategy should an enterprise webhook platform use when customer endpoints fail?
3. Why must a webhook delivery engine enforce strict connection timeouts on every outbound HTTP request?

## What comes next
Having understood project: webhook delivery platform, we next discover its inherent boundaries and transition to **Project: Multi-Tenant SaaS Backend**.
