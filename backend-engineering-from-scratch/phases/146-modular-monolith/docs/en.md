# Lesson 146: Modular Monolith

> **Motto**: A modular monolith enforces strict boundaries between domain modules within a single deployable codebase.

---

## Motto
"A modular monolith enforces strict boundaries between domain modules within a single deployable codebase."

## Problem
Unconstrained monoliths devolve into a 'big ball of mud' where any module queries any other module's private database tables.

## Prediction
Enforcing explicit public interfaces between modules (Users, Orders, Billing) prevents spaghetti dependencies.

## Why this matters
A modular monolith gives you the boundary isolation of microservices with the deployment simplicity of a monolith.

## First principles
Module Boundary: Module A communicates with Module B ONLY through B's public interface; direct DB access is forbidden.

## Mental model
```text
Module: Orders [Internal Service, Private Tables] <── Public Interface ──> Module: Users [Internal Service, Private Tables]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Python packages with explicit `__all__` interfaces and dependency boundary rules.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/146-modular-monolith/tests/ -v
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
- **Failure Injection**: Attempt to import an internal private repository of the `users` module inside the `orders` module.
- Execute the experiment script:
```bash
python phases/146-modular-monolith/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Architectural boundary test detects illegal cross-module import and fails the build.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Each module should own its own database tables; never join tables belonging to another module directly in SQL.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Modular monoliths make future service extraction trivial: the module is already cleanly isolated behind an interface.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Enforce module boundaries in CI using static analysis tools like `import-linter`.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. How does a modular monolith prevent the 'big ball of mud' architecture?
2. Why should Module A never execute SQL JOINs against database tables owned by Module B?
3. How do static architectural linting tools enforce module boundaries in CI pipelines?

## What comes next
Having understood modular monolith, we next discover its inherent boundaries and transition to **When to Split a Service**.
