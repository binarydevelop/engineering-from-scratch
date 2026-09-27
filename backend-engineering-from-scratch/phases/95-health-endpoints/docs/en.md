# Lesson 95: Health Endpoints

> **Motto**: Health endpoints report process and dependency status to container orchestrators, governing traffic routing and restarts.

---

## Motto
"Health endpoints report process and dependency status to container orchestrators, governing traffic routing and restarts."

## Problem
A health endpoint that executes heavy database queries on every probe consumes database connections and causes self-inflicted outages.

## Prediction
Separating `/health/live` (is process running?) from `/health/ready` (is pool connected?) prevents unnecessary container restarts.

## Why this matters
Proper health checks enable zero-downtime rolling deployments and automated recovery from stalled processes.

## First principles
Liveness Probe: If failing, restart container. Readiness Probe: If failing, stop sending traffic but do NOT restart.

## Mental model
```text
Kubernetes -> GET /health/live (200 OK: Don't restart) -> GET /health/ready (200 OK: Route user traffic)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI `/health/live` and `/health/ready` endpoints.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/95-health-endpoints/tests/ -v
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
- **Failure Injection**: Sever database connection; query liveness and readiness endpoints.
- Execute the experiment script:
```bash
python phases/95-health-endpoints/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Liveness returns 200 OK (process alive, don't restart); Readiness returns 503 (database disconnected, drain traffic).
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never perform slow, expensive operations in health checks; checks run every few seconds and must complete in < 50ms.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Protect detailed readiness diagnosis from public view to prevent leaking internal database hostnames and statuses.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: During application boot, readiness must return 503 until migrations and connection pools are fully initialized.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the critical operational difference between a Liveness probe and a Readiness probe?
2. What disaster happens when a Liveness probe checks a slow external database that is temporarily overloaded?
3. Why should health check endpoints complete in under 50 milliseconds?

## What comes next
Having understood health endpoints, we next discover its inherent boundaries and transition to **Observability Debugging**.
