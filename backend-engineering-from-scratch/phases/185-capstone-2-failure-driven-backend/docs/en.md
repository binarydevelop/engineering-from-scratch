# Lesson 185: Capstone 2: Failure-Driven Backend

> **Motto**: Subject Capstone 1 to aggressive chaos engineering and failure injection, proving resilience under real-world outages.

---

## Motto
"Subject Capstone 1 to aggressive chaos engineering and failure injection, proving resilience under real-world outages."

## Problem
A backend is only as reliable as its behavior when dependencies fail; untested resilience is wishful thinking.

## Prediction
Deliberately severing databases, crashing Redis, injecting timeouts, and exhausting pools proves system survival.

## Why this matters
This capstone proves that the system degrades gracefully, fails fast, and self-heals under catastrophic conditions.

## First principles
Predict -> Inject Fault (DB Down / Redis Down / Slow API / Worker Crash) -> Observe Telemetry -> Diagnose -> Verify Recovery.

## Mental model
```text
Chaos Injector ──[Drop Redis / Sever DB / Inject 5s Latency]──> Capstone Monolith ──> Verify Fail-Open & Circuit Breaker
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Chaos engineering and resilience verification harness.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/185-capstone-2-failure-driven-backend/tests/ -v
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
- **Failure Injection**: Run the full chaos test suite injecting 10 failure modes: database drop, cache crash, worker kill, slow external dependency.
- Execute the experiment script:
```bash
python phases/185-capstone-2-failure-driven-backend/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify system behaves according to prediction: non-critical paths degrade gracefully; critical paths fail fast with proper status codes.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Verify that when degraded dependencies recover, the application automatically restores full operational performance.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Ensure alert metrics fire accurately during every simulated failure mode.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Document the empirical failure behavior and recovery timeline for each scenario in the evidence log.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What happens to Capstone 1 when the Redis cache cluster is completely severed?
2. How does Capstone 1 isolate slow external dependencies to prevent cascading worker thread exhaustion?
3. What evidence proves that Capstone 1 self-heals when a failed dependency returns online?

## What comes next
Having understood capstone 2: failure-driven backend, we next discover its inherent boundaries and transition to **Capstone 3: Extract One Service**.
