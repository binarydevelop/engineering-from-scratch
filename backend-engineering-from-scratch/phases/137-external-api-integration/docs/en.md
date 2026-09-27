# Lesson 137: External API Integration

> **Motto**: Defensive API adapters wrap third-party HTTP integrations, isolating external data contracts, errors, and outages.

---

## Motto
"Defensive API adapters wrap third-party HTTP integrations, isolating external data contracts, errors, and outages."

## Problem
Scattering direct HTTP calls to Stripe, Twilio, or SendGrid throughout business logic creates tight coupling and fragility.

## Prediction
Encapsulating external calls behind typed adapter interfaces isolates error mapping, timeouts, and mocking.

## Why this matters
Defensive adapters protect domain logic when third-party providers change their API schemas or suffer outages.

## First principles
Domain Service -> PaymentGateway Interface -> StripeAdapter (HTTP Client, Timeouts, Error Mapping) -> External API.

## Mental model
```text
Order Service ──> [PaymentGateway Adapter] ──[Defensive Bounds / Timeouts]──> Third-Party Payment API
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: HTTPX client wrappers with domain exception mapping.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/137-external-api-integration/tests/ -v
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
- **Failure Injection**: Simulate a third-party API returning an unexpected 502 Bad Gateway with an HTML error page.
- Execute the experiment script:
```bash
python phases/137-external-api-integration/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Adapter intercepts raw error, prevents HTML from bubbling up, and raises typed `PaymentGatewayUnavailableException`.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never leak third-party provider exceptions or error schemas into core application domain logic.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Always write mock adapter implementations to enable fast, offline testing of domain services without hitting external APIs.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Log outbound request IDs, durations, and status codes to monitor third-party provider SLA compliance.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should third-party HTTP calls never be made directly inside domain business logic?
2. What is the role of an Adapter pattern in shielding applications from third-party schema changes?
3. How do mock adapter implementations speed up integration testing and reduce external API costs?

## What comes next
Having understood external api integration, we next discover its inherent boundaries and transition to **Payment-Like Workflow**.
