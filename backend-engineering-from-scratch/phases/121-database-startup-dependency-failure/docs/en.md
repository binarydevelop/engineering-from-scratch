# Lesson 121: Database Startup / Dependency Failure

> **Motto**: Application boot must tolerate slow database startup by implementing retry-with-backoff connection loops.

---

## Motto
"Application boot must tolerate slow database startup by implementing retry-with-backoff connection loops."

## Problem
When an application container starts faster than its database container, it crashes immediately, triggering crash loops.

## Prediction
Building a startup readiness probe that retries the database connection with exponential backoff makes boot robust.

## Why this matters
Boot resiliency eliminates deployment race conditions and avoids reliance on fragile startup order assumptions.

## First principles
Container Starts -> Attempt DB Connect -> Connection Refused -> Wait 1s -> Retry -> Success -> Application Starts Serving.

## Mental model
```text
App Boot -> DB Not Ready (Wait 1s) -> DB Not Ready (Wait 2s) -> DB Ready! -> Initialize Pools -> Start HTTP Listener
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Lifespan event startup validation in FastAPI.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/121-database-startup-dependency-failure/tests/ -v
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
- **Failure Injection**: Start the application server while the database is completely offline; observe graceful retry loop in logs.
- Execute the experiment script:
```bash
python phases/121-database-startup-dependency-failure/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Start the database after 3 seconds; observe application discovers database, completes initialization, and starts serving.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Set a maximum total startup timeout (e.g. 60 seconds); fail fast if the database remains unreachable after the deadline.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Container orchestrators like Kubernetes restart crashing containers, but startup retries avoid unnecessary container restarts.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Log clear, human-readable startup progress: 'Waiting for database at localhost:5432... (Attempt 2/10)'.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why does an application container frequently crash when started simultaneously with a database container in Docker Compose?
2. How does an exponential backoff connection loop at application startup solve the startup race condition?
3. Why should a startup retry loop still enforce a maximum timeout deadline?

## What comes next
Having understood database startup / dependency failure, we next discover its inherent boundaries and transition to **Migrations During Deployment**.
