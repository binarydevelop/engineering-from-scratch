# Lesson 109: Timeout Cascades

> **Motto**: A timeout cascade occurs when a slow downstream service causes upstream caller threads to back up, crashing the entire architecture.

---

## Motto
"A timeout cascade occurs when a slow downstream service causes upstream caller threads to back up, crashing the entire architecture."

## Problem
Service A calls Service B with a 60-second timeout; Service B slows down; Service A workers accumulate waiting, exhausting all threads.

## Prediction
Enforcing short timeouts, strict deadlines, and circuit breakers isolates the slow service and stops the cascade.

## Why this matters
Understanding cascades explains why a minor outage in a non-critical microservice can bring down an entire enterprise.

## First principles
Service C slows to 10s -> Service B threads wait 10s (saturates) -> Service A threads wait 10s (saturates) -> Ingress collapses.

## Mental model
```text
Client -> Gateway (Saturated) -> Order Service (Saturated) -> Inventory Service (Saturated) -> Slow Third-Party API
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Distributed deadline propagation and circuit breaker protection.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/109-timeout-cascades/tests/ -v
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
- **Failure Injection**: Inject a 5-second delay into Service C with a 10-second timeout in Service A; bombard with traffic.
- Execute the experiment script:
```bash
python phases/109-timeout-cascades/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe Service A thread pool completely exhaust within 2 seconds; all unrelated endpoints on Service A crash.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Apply defensive timeouts (500ms) and circuit breakers; observe Service A sheds failing dependency and keeps serving other traffic.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Propagate remaining deadline budgets across HTTP calls: if total deadline is 2s and 1.5s has elapsed, downstream timeout is 500ms.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Cascading timeouts are the primary reason microservices fail in chain reactions; isolate failure boundaries strictly.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is a cascading failure and how does a slow downstream service trigger it?
2. Why are long timeouts (e.g. 60 seconds) an operational hazard in distributed systems?
3. How does distributed deadline propagation prevent downstream services from wasting work on already timed-out requests?

## What comes next
Having understood timeout cascades, we next discover its inherent boundaries and transition to **Failure Injection**.
