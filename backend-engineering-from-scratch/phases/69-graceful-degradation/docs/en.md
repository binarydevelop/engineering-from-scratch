# Lesson 69: Graceful Degradation

> **Motto**: Graceful degradation returns degraded or cached fallback results when non-critical dependencies fail, maintaining core service.

---

## Motto
"Graceful degradation returns degraded or cached fallback results when non-critical dependencies fail, maintaining core service."

## Problem
Failing the entire e-commerce checkout page because the product recommendations service is down is a severe design flaw.

## Prediction
Returning fallback data (empty recommendations, cached inventory status) allows the customer to complete their primary goal.

## Why this matters
Graceful degradation prioritizes business continuity over secondary perfection.

## First principles
Request -> Fetch Core Data (Mandatory) + Fetch Recommendations (Optional) -> Recommendations Fails -> Return Core Data!

## Mental model
```text
Full Page (Core + Recs) ──[Recs Outage]──> Degraded Page (Core + 'Recommendations temporarily unavailable')
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI endpoint implementing try-fallback blocks around non-critical dependencies.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/69-graceful-degradation/tests/ -v
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
- **Failure Injection**: Disable the recommendation service completely and execute checkout requests.
- Execute the experiment script:
```bash
python phases/69-graceful-degradation/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert that checkout succeeds with HTTP 200; response contains order confirmation and a graceful fallback note.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Categorize dependencies explicitly: Critical (must fail request if broken) vs Non-Critical (must degrade gracefully).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Degraded responses must emit telemetry so engineers know a fallback is active while users continue working.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Graceful degradation requires explicit product alignment: product managers must decide acceptable fallback states.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why should an e-commerce checkout never fail because a personalized recommendations engine is down?
2. How do you distinguish a critical dependency from a non-critical dependency in system design?
3. What operational signals must be emitted when a service operates in a degraded fallback state?

## What comes next
Having understood graceful degradation, we next discover its inherent boundaries and transition to **Concurrency Model**.
