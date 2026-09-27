# Lesson 97: Testing Pyramid / Strategy

> **Motto**: A balanced testing strategy combines fast unit tests, realistic integration tests, and focused API contract tests.

---

## Motto
"A balanced testing strategy combines fast unit tests, realistic integration tests, and focused API contract tests."

## Problem
Relying solely on slow, flaky end-to-end browser tests slows CI pipelines to a crawl and delays shipping.

## Prediction
Structuring test suites into Unit (fast, isolated), Integration (real database), and API tests yields confidence and speed.

## Why this matters
A disciplined test pyramid catches bugs within seconds locally rather than after deployment.

## First principles
Pyramid: Unit Tests (70%: Pure logic, microseconds) -> Integration (20%: Real SQL/Redis) -> API/E2E (10%: Full stack).

## Mental model
```text
Unit (Thousands in 2s) ──> Integration (Hundreds in 10s) ──> API/E2E (Dozens in 30s)
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Pytest test discovery, markers (`@pytest.mark.unit`, `@pytest.mark.integration`), and configuration.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/97-testing-pyramid-strategy/tests/ -v
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
- **Failure Injection**: Run the entire unit test suite; assert 100 tests pass in under 500ms with zero database dependencies.
- Execute the experiment script:
```bash
python phases/97-testing-pyramid-strategy/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Run the integration suite with real SQLite/PostgreSQL; assert database constraints and queries are validated.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Never mock database behavior that matters (transactions, constraints, unique keys); use real test databases.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Flaky tests destroy team confidence in CI; quarantine flaky tests immediately until deterministically fixed.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Test coverage metrics: target high coverage on complex domain invariants; don't chase 100% on boilerplate DTOs.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the three tiers of the backend testing pyramid and what is the specific role of each?
2. Why is mocking database constraints in unit tests dangerous for data integrity?
3. How does test execution speed directly affect developer iteration velocity?

## What comes next
Having understood testing pyramid / strategy, we next discover its inherent boundaries and transition to **Unit Testing Business Logic**.
