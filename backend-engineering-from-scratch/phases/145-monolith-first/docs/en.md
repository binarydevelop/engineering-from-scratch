# Lesson 145: Monolith First

> **Motto**: A well-structured monolith is the fastest, simplest, and most reliable deployment architecture for 95% of engineering problems.

---

## Motto
"A well-structured monolith is the fastest, simplest, and most reliable deployment architecture for 95% of engineering problems."

## Problem
Starting a new project as 15 distributed microservices introduces massive networking, serialization, and deployment complexity before understanding domain boundaries.

## Prediction
Building a unified monolith first maximizes feature velocity, simplifies ACID transactions, and eliminates distributed network fallacies.

## Why this matters
Premature microservices kill startups; successful companies start with monoliths and only split when organizationally necessary.

## First principles
Monolith: Single codebase, single deployment, in-memory function calls, local ACID transactions. Zero network serialization between modules.

## Mental model
```text
Client -> Ingress -> Monolithic Deployable [Users Module + Catalog Module + Orders Module] -> PostgreSQL
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Unified FastAPI deployment architectures.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/145-monolith-first/tests/ -v
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
- **Failure Injection**: Benchmark latency of in-memory function calls between modules vs simulated network microservice HTTP calls.
- Execute the experiment script:
```bash
python phases/145-monolith-first/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe in-memory function call takes 0.001ms; remote HTTP microservice call takes 15ms (15,000x slower).
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: A monolith does NOT mean spaghetti code: modular monoliths enforce strict internal package and interface boundaries.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Deploying a monolith requires a single CI/CD pipeline, single container, and simple monitoring.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Only consider splitting services when team size or scaling requirements strictly mandate organizational decoupling.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why do in-memory function calls within a monolith execute 10,000x faster than network calls between microservices?
2. What operational and deployment overheads are introduced when splitting a monolith into microservices?
3. What is the difference between a messy spaghetti monolith and a well-architected modular monolith?

## What comes next
Having understood monolith first, we next discover its inherent boundaries and transition to **Modular Monolith**.
