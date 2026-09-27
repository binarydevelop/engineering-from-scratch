# Lesson 98: Unit Testing Business Logic

> **Motto**: Unit tests verify pure domain invariants in memory without network sockets, databases, or external dependencies.

---

## Motto
"Unit tests verify pure domain invariants in memory without network sockets, databases, or external dependencies."

## Problem
Coupling business rules to database tables makes running unit tests require local databases and slow down by 100x.

## Prediction
Keeping domain models and business calculations pure enables running thousands of unit tests per second.

## Why this matters
Fast unit tests provide instant developer feedback during refactoring and domain modeling.

## First principles
Input Domain Model -> Pure Business Function -> Output Domain Model. Zero I/O, zero network, zero mocks.

## Mental model
```text
OrderEntity(items, discount) -> calculate_total() -> Assert total == Expected in 0.05 milliseconds
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pytest test fixtures for domain entity construction.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/98-unit-testing-business-logic/tests/ -v
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
- **Failure Injection**: Run 50 domain unit tests verifying complex discount and pricing matrix invariants.
- Execute the experiment script:
```bash
python phases/98-unit-testing-business-logic/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Assert all 50 tests execute in < 20 milliseconds with zero network or disk access.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Design domain functions to be deterministic: pass current time and random seeds as explicit parameters.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Unit tests must be completely isolated; no test should depend on the execution order or side effects of another.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Unit test edge cases thoroughly: negative numbers, zero balances, empty collections, extreme string lengths.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must domain unit tests run without spinning up an HTTP server or database connection?
2. How does passing explicit timestamps into business functions make temporal logic deterministically testable?
3. What domain rules in an e-commerce backend are prime candidates for pure unit testing?

## What comes next
Having understood unit testing business logic, we next discover its inherent boundaries and transition to **Repository Integration Tests**.
