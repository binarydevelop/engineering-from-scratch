# Lesson 135: Webhooks

> **Motto**: Outbound webhooks notify external client systems of events by sending HTTP POST requests to client-registered URLs.

---

## Motto
"Outbound webhooks notify external client systems of events by sending HTTP POST requests to client-registered URLs."

## Problem
Polling an API for status updates wastes bandwidth; webhooks push data to clients immediately upon state change.

## Prediction
Building a reliable webhook engine requires durable queues, retries with exponential backoff, and failure isolation.

## Why this matters
Webhooks power the modern API ecosystem, connecting payment gateways, CI pipelines, and SaaS integrations.

## First principles
Event Occurs (Payment Succeeded) -> Enqueue Webhook Delivery Task -> Worker sends HTTP POST to Client Endpoint -> Handle Response.

## Mental model
```text
Event Triggered -> Queue Delivery Task -> HTTP POST to https://client.com/webhook -> Success (2xx) or Retry with Backoff
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Asynchronous webhook dispatchers in production backends.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/135-webhooks/tests/ -v
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
- **Failure Injection**: Register a webhook endpoint; trigger a domain event; observe webhook delivery worker sends formatted HTTP POST payload.
- Execute the experiment script:
```bash
python phases/135-webhooks/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Simulate client endpoint returning HTTP 503; verify worker retries delivery up to 5 times with exponential backoff.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always enforce strict HTTP connect and read timeouts (<= 5s) on webhook deliveries: client servers may be slow or hung.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Isolate webhook delivery in background workers; never send outbound webhooks synchronously inside user HTTP request handlers.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Disable endpoints that fail continuously for several days to prevent wasting resources on abandoned customer URLs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must outbound webhook deliveries always be executed asynchronously by background workers?
2. How should a webhook delivery system handle a client receiver endpoint that returns HTTP 500 or times out?
3. Why is it essential to enforce strict connection timeouts when calling customer-configured webhook URLs?

## What comes next
Having understood webhooks, we next discover its inherent boundaries and transition to **Webhook Verification**.
