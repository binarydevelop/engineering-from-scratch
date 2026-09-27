# Lesson 55: Retry

> **Motto**: Transient failures happen; automated retries with bounded limits and backoff allow background workers to self-heal.

---

## Motto
"Transient failures happen; automated retries with bounded limits and backoff allow background workers to self-heal."

## Problem
Failing a task permanently on the first temporary network hiccup causes massive false-positive operational failures.

## Prediction
Implementing automatic retries with exponential delays handles temporary database locks and third-party timeouts.

## Why this matters
Resilient workers recover from transient network blips without requiring human operator intervention.

## First principles
Failure -> Check Retry Count < MaxRetries -> Schedule Retry with Delay -> Success or Escalate.

## Mental model
```text
Job Fails -> Attempt 1 (1s delay) -> Fails -> Attempt 2 (4s delay) -> Fails -> Attempt 3 (16s delay) -> Success!
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Celery / ARQ retry decorators with max_retries and countdown intervals.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/55-retry/tests/ -v
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
- **Failure Injection**: Simulate a third-party service that fails on the first 2 attempts and succeeds on the 3rd attempt.
- Execute the experiment script:
```bash
python phases/55-retry/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Worker catches transient error, schedules retry, logs attempts, and succeeds on attempt 3 without data loss.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always set a hard maximum retry limit (e.g. 3 or 5); never retry infinitely.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Retrying non-idempotent operations (charging a credit card) can cause disastrous duplicate financial charges.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Retries must be coupled with backoff; retrying immediately in a tight loop hammers failing dependencies into collapse.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must automated retries never retry infinitely?
2. What types of errors are safe to retry (transient) versus errors that should fail immediately (permanent)?
3. What disaster occurs when a non-idempotent task is retried after a network timeout?

## What comes next
Having understood retry, we next discover its inherent boundaries and transition to **Idempotent Jobs**.
