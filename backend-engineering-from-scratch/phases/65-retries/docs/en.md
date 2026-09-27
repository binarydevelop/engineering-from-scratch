# Lesson 65: Retries

> **Motto**: Retries must be restricted strictly to idempotent operations and transient network failures; retrying blindly causes disaster.

---

## Motto
"Retries must be restricted strictly to idempotent operations and transient network failures; retrying blindly causes disaster."

## Problem
Retrying a non-idempotent operation on network timeout causes duplicate charges; retrying a 400 Bad Request wastes CPU.

## Prediction
Classifying errors into transient (503, connect error) vs permanent (400, 401, 404, 422) ensures retries are safe and effective.

## Why this matters
Selective retries recover from temporary glitches without aggravating permanent system failures.

## First principles
Is Error Transient? YES -> Is Operation Idempotent? YES -> RETRY with Backoff. Otherwise: FAIL FAST.

## Mental model
```text
Network Glitch -> Check Error Code (503 Service Unavailable) -> Safe to retry -> Wait & Retry -> Success
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Tenacity library integration with FastAPI external dependency clients.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/65-retries/tests/ -v
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
- **Failure Injection**: Simulate a permanent HTTP 400 Bad Request error; verify client fails immediately without retrying.
- Execute the experiment script:
```bash
python phases/65-retries/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Simulate a transient HTTP 503 error on an idempotent GET; verify client retries and recovers.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never retry non-idempotent mutations (POST) unless guaranteed safe by an Idempotency Key.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unchecked retries against an overloaded server act as a distributed denial of service attack against yourself.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Retries must always decrement from an overall deadline budget to prevent indefinite execution.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must HTTP 4xx client errors NEVER be retried automatically?
2. Under what exact conditions is an automatic retry safe in distributed systems?
3. How can automated retries accidentally take down an already struggling downstream service?

## What comes next
Having understood retries, we next discover its inherent boundaries and transition to **Exponential Backoff and Jitter**.
