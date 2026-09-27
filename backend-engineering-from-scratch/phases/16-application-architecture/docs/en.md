# Lesson 16: Application Architecture

> **Motto**: Layered architecture isolates transport protocols from business rules, allowing either to change without destroying the other.

---

## Motto
"Layered architecture isolates transport protocols from business rules, allowing either to change without destroying the other."

## Problem
Placing business rules, database queries, and HTTP headers in one giant route function leads to unmaintainable spaghetti.

## Prediction
Separating HTTP transport from Application Services and Domain Invariants creates modular, readable backends.

## Why this matters
Clean boundaries enable painless database migrations, framework upgrades, and isolated unit testing.

## First principles
Domain Model (pure business rules) <- Application Service (use cases) <- Transport Controller (HTTP/CLI).

## Mental model
```text
HTTP Route -> Application Use-Case Service -> Pure Domain Entity -> Repository Interface -> Database Adapter
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI router invoking an OrderApplicationService injecting an OrderRepository.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/16-application-architecture/tests/ -v
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
- **Failure Injection**: Attempt to import framework HTTP request objects inside the domain entity layer.
- Execute the experiment script:
```bash
python phases/16-application-architecture/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Enforce architectural boundary check verifying that domain modules have zero external dependencies.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep domain models completely free of database ORM annotations and HTTP constructs.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Security controls belong in application services; never delegate authorization to transport controllers alone.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Single-file services are fine for tiny prototypes; modular layers become mandatory when teams scale.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must domain entities never import web framework or HTTP request libraries?
2. What is the specific responsibility of an Application Service versus a Domain Entity?
3. How does dependency inversion protect core business logic from database schema changes?

## What comes next
Having understood application architecture, we next discover its inherent boundaries and transition to **Business Logic vs HTTP Logic**.
