# Lesson 67: Circuit Breaker

> **Motto**: A circuit breaker detects repeated downstream failures and trips open, failing fast to protect both caller and dependency.

---

## Motto
"A circuit breaker detects repeated downstream failures and trips open, failing fast to protect both caller and dependency."

## Problem
When an external service goes down, caller requests pile up waiting for timeouts, exhausting threads and crashing the caller.

## Prediction
Tripping a circuit breaker stops outbound traffic immediately, returning fast fallbacks and giving the dependency time to recover.

## Why this matters
Circuit breakers isolate failure domains and prevent catastrophic cascading collapses across service graphs.

## First principles
States: CLOSED (normal operation) -> OPEN (fail fast immediately) -> HALF-OPEN (test single probe request).

## Mental model
```text
Failures > Threshold -> OPEN (Return fallback in 0.1ms) -> Wait Cool-off -> HALF-OPEN (Probe) -> Success -> CLOSED
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: PyBreaker / Aiobreaker integration for external API dependencies.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/67-circuit-breaker/tests/ -v
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
- **Failure Injection**: Inject continuous failures on an external dependency until the failure threshold (e.g. 5 errors) is reached.
- Execute the experiment script:
```bash
python phases/67-circuit-breaker/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe state transition to OPEN; subsequent requests return fallback immediately without calling dependency.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Tune cool-down periods and half-open probe counts to prevent premature circuit closing.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Circuit breaker metrics (trip count, state) must be exposed via Prometheus to alert on dependency degradation.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Combine circuit breakers with graceful fallback responses (e.g. return cached recommendations or empty list).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the three states of a Circuit Breaker and what triggers transitions between them?
2. How does an open circuit breaker prevent cascading thread pool exhaustion in the caller?
3. What is the role of the Half-Open state in circuit breaker recovery?

## What comes next
Having understood circuit breaker, we next discover its inherent boundaries and transition to **Bulkheads**.
