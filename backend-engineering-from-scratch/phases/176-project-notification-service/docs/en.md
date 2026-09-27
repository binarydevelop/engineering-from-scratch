# Lesson 176: Project: Notification Service

> **Motto**: Build a multi-channel notification microservice with templates, provider adapters, rate-limiting guards, and delivery retries.

---

## Motto
"Build a multi-channel notification microservice with templates, provider adapters, rate-limiting guards, and delivery retries."

## Problem
Coupling notification delivery directly into business services causes outages when email/SMS providers experience downtime.

## Prediction
Decoupling notifications behind a queue with multi-provider fallbacks and rate limiting guarantees reliable delivery.

## Why this matters
Notification services power customer communications across email, SMS, and push channels at enterprise scale.

## First principles
API -> Enqueue Notification -> Worker renders Jinja2 template -> Dispatches via Provider Adapter -> Retries on error.

## Mental model
```text
Enqueue Notification -> Worker -> Template Engine -> Primary Provider (SES) ──[Fails]──> Backup Provider (SendGrid)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Multi-channel notification microservice architecture.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/176-project-notification-service/tests/ -v
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
- **Failure Injection**: Enqueue 100 email notifications; simulate primary provider outage; observe worker automatically switches to backup adapter.
- Execute the experiment script:
```bash
python phases/176-project-notification-service/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify all 100 emails are delivered successfully; verify user unsubscribe preferences are strictly enforced.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Enforce global and per-user rate limits to prevent flooding users during automated retry storms.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Isolate provider API keys inside secure environment variables; never hardcode credentials in notification templates.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Support asynchronous delivery status webhooks from providers to update notification status in database.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does decoupling notifications into an asynchronous microservice protect core business APIs from third-party outages?
2. What adapter patterns allow switching between SendGrid, Mailgun, and AWS SES without changing domain code?
3. How do webhook callbacks from email providers maintain sender reputation by handling bounces and spam complaints?

## What comes next
Having understood project: notification service, we next discover its inherent boundaries and transition to **Project: File Processing Service**.
