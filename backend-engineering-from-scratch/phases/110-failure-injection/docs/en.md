# Lesson 110: Failure Injection

> **Motto**: Chaos engineering and failure injection test system resilience by deliberately introducing real network and database faults.

---

## Motto
"Chaos engineering and failure injection test system resilience by deliberately introducing real network and database faults."

## Problem
Assuming error handling works without testing it in production-like conditions guarantees surprises during real outages.

## Prediction
Injecting artificial latency, dropped database connections, packet loss, and killed processes proves recovery mechanisms.

## Why this matters
Failure injection turns resilience from hopeful theoretical speculation into verified empirical engineering.

## First principles
Hypothesis: 'System handles Redis failure gracefully' -> Inject Fault (Kill Redis) -> Observe -> Measure -> Verify.

## Mental model
```text
Chaos Injector ──[Sever DB Socket / Drop Redis]──> Application Service ──> Verify Fail-Open / Fallback Behavior
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Chaos engineering frameworks and fault-tolerant middleware.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/110-failure-injection/tests/ -v
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
- **Failure Injection**: Inject 2,000ms latency on the database; verify that application timeout triggers cleanly at 500ms and returns HTTP 504.
- Execute the experiment script:
```bash
python phases/110-failure-injection/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Inject complete Redis outage; verify that cache-aside gracefully falls back to database reads without throwing 500 errors.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Always run failure injection against automated test suites before deploying to production environments.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Test game days: periodically inject faults in staging environments to verify on-call team alerting and runbooks.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Failure injection proves that degraded fallbacks and circuit breakers actually work as designed.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the core philosophy of Chaos Engineering and failure injection?
2. What four specific failure modes should every production backend be tested against?
3. How does failure injection prove whether a system fails open or fails closed?

## What comes next
Having understood failure injection, we next discover its inherent boundaries and transition to **Configuration**.
