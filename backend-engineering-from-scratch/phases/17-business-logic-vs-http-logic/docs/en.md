# Lesson 17: Business Logic vs HTTP Logic

> **Motto**: Business rules represent real-world enterprise invariants; HTTP logic merely encodes how those rules are triggered over the network.

---

## Motto
"Business rules represent real-world enterprise invariants; HTTP logic merely encodes how those rules are triggered over the network."

## Problem
When business logic is locked inside route functions, it cannot be run from background jobs, CLI commands, or message handlers.

## Prediction
Extracting logic into pure Python functions enables sub-millisecond unit testing without spinning up HTTP servers.

## Why this matters
Decoupled business logic can be shared across web APIs, gRPC endpoints, and batch processing pipelines.

## First principles
An enterprise invariant (e.g. 'Order total cannot be negative') exists independently of HTTP status codes.

## Mental model
```text
HTTP Handler: Reads Headers, Parses JSON, Calls Service -> Domain Service: Calculates Tax, Enforces Discounts, Mutates Entity
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: FastAPI endpoint delegating directly to a pure domain calculation function.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/17-business-logic-vs-http-logic/tests/ -v
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
- **Failure Injection**: Execute unit tests against domain logic without starting a test client or socket server.
- Execute the experiment script:
```bash
python phases/17-business-logic-vs-http-logic/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Observe tests completing in < 1ms compared to 20ms+ for full HTTP roundtrip tests.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Structure domain methods to return explicit Result or DomainError types rather than raising HTTPExceptions.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never trust input formatting even if client-side validation passed; domain invariants are the ultimate defense.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Decoupled domain rules can be audited by domain experts without understanding web networking.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why is testing domain logic directly 100x faster than testing via an HTTP test client?
2. How does raising domain exceptions inside route handlers enable clean HTTP status code mapping?
3. What happens when a background worker needs to run business logic that was embedded in a FastAPI route?

## What comes next
Having understood business logic vs http logic, we next discover its inherent boundaries and transition to **PostgreSQL Integration**.
