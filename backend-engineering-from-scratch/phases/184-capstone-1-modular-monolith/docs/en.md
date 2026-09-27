# Lesson 184: Capstone 1: Production-Grade Modular Monolith

> **Motto**: Synthesize all backend engineering disciplines into a production-grade modular monolith with auth, catalog, orders, and telemetry.

---

## Motto
"Synthesize all backend engineering disciplines into a production-grade modular monolith with auth, catalog, orders, and telemetry."

## Problem
Fragmenting a system into microservices before mastering monolithic architecture produces distributed chaos.

## Prediction
Building a unified, production-ready modular monolith demonstrates how all backend layers integrate into a cohesive whole.

## Why this matters
This capstone serves as the complete, production-ready reference architecture for modern backend systems.

## First principles
Modular Monolith: Ingress -> Auth & Security -> Modules (Users, Catalog, Orders, Notifications) -> PostgreSQL, Redis, Outbox.

## Mental model
```text
Client ──> Modular Monolith [Auth -> Validation -> Orders Module -> SQL Tx + Outbox -> Async Worker -> Redis/Metrics]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Full production modular monolith application.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/184-capstone-1-modular-monolith/tests/ -v
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
- **Failure Injection**: Execute comprehensive integration and load test suite verifying authentication, concurrent checkout, outbox events, and telemetry.
- Execute the experiment script:
```bash
python phases/184-capstone-1-modular-monolith/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert zero concurrency errors under 50 simultaneous checkouts; verify all outbox events are published and processed.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Strict module boundaries: modules communicate exclusively via defined interfaces; zero cross-module database table joins.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Expose full RED metrics (`/metrics`), structured JSON logging, and correlation ID propagation across all modules.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Containerized with a production multi-stage Dockerfile running as an unprivileged user.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does Capstone 1 enforce modular boundaries between the Users, Catalog, and Orders domains?
2. How does the Transactional Outbox pattern inside Capstone 1 guarantee asynchronous event delivery without dual-write bugs?
3. What telemetry and observability endpoints are exposed by Capstone 1 for production monitoring?

## What comes next
Having understood capstone 1: production-grade modular monolith, we next discover its inherent boundaries and transition to **Capstone 2: Failure-Driven Backend**.
