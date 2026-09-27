# Lesson 15: Dependency Injection

> **Motto**: Dependency injection decouples application handlers from concrete infrastructure, enabling modularity and deterministic testing.

---

## Motto
"Dependency injection decouples application handlers from concrete infrastructure, enabling modularity and deterministic testing."

## Problem
Hardcoding global database connections and third-party API clients makes handlers untestable and impossible to mock.

## Prediction
Passing database sessions and external services as explicit parameters allows instant substitution during unit testing.

## Why this matters
DI eliminates hidden global state, manages resource lifecycles cleanly, and separates construction from execution.

## First principles
Components should declare what they need, not construct how they obtain it (Inversion of Control).

## Mental model
```text
Container / Factory -> Instantiate Dependencies -> Inject into Handler -> Execute -> Finalize / Cleanup
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI Depends() mechanism injecting database sessions and authentication principals.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/15-dependency-injection/tests/ -v
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
- **Failure Injection**: Swap a real PostgreSQL repository with an in-memory mock repository in a unit test.
- Execute the experiment script:
```bash
python phases/15-dependency-injection/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Execute handler tests at 100x speed without running network sockets or external databases.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Use context managers inside dependencies to guarantee resource closure (e.g. database session rollback/close).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Avoid injecting wide 'god objects' or service locators that obscure actual dependency requirements.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Scoped dependencies must be cleaned up promptly per request to avoid resource leaks.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the difference between Dependency Injection and a Service Locator anti-pattern?
2. How does FastAPI Depends() manage the cleanup of database connections via yield?
3. Why does global mutable state make concurrent backend testing impossible?

## What comes next
Having understood dependency injection, we next discover its inherent boundaries and transition to **Application Architecture**.
