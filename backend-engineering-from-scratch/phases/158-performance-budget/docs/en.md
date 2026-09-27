# Lesson 158: Performance Budget

> **Motto**: A performance budget decomposes an end-to-end latency SLA into allocated time budgets across every layer of the request path.

---

## Motto
"A performance budget decomposes an end-to-end latency SLA into allocated time budgets across every layer of the request path."

## Problem
Allowing every middleware, database query, and external call to take arbitrary time results in sluggish 2-second API responses.

## Prediction
Establishing strict time budgets (e.g. Total 200ms = Ingress 10ms, Auth 15ms, DB 40ms, App 15ms, Buffer 120ms) enforces discipline.

## Why this matters
Performance budgets prevent gradual latency creep and guide optimization priorities.

## First principles
Total Budget: 100ms. Ingress/TLS: 10ms. Auth/Middleware: 10ms. DB Queries: 40ms. Domain Logic: 15ms. Serialization: 10ms. Slack: 15ms.

## Mental model
```text
Budget: [Ingress: 10ms] + [Middleware: 10ms] + [SQL: 40ms] + [App: 15ms] + [Serialize: 10ms] = 85ms <= 100ms (Within Budget)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Distributed tracing span budget assertions.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/158-performance-budget/tests/ -v
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
- **Failure Injection**: Execute a request where a database query takes 65ms against a 40ms budget; profiler flags budget overrun.
- Execute the experiment script:
```bash
python phases/158-performance-budget/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Isolate the offending layer immediately; optimize query to bring total execution back within the 100ms performance budget.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Set automated performance budget assertions in CI integration tests to prevent merging slow code.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Allocate a conservative safety buffer (slack) in performance budgets to absorb network jitter and garbage collection pauses.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Budget for p95 and p99 latency targets, not arithmetic averages.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is an architectural performance budget and why is it decomposed across lifecycle layers?
2. What happens to end-to-end latency when individual microservice teams lack strict performance budgets?
3. How can performance budget violations be caught automatically in Continuous Integration pipelines?

## What comes next
Having understood performance budget, we next discover its inherent boundaries and transition to **Backend Anti-Patterns**.
