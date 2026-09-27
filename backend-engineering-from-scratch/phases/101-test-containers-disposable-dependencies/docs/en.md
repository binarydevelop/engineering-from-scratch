# Lesson 101: Test Containers / Disposable Dependencies

> **Motto**: Disposable test containers provide isolated, ephemeral PostgreSQL and Redis instances for completely reproducible testing.

---

## Motto
"Disposable test containers provide isolated, ephemeral PostgreSQL and Redis instances for completely reproducible testing."

## Problem
Running integration tests against a long-lived dirty database causes tests to fail due to leftover test data.

## Prediction
Spinning up clean Docker containers per test run guarantees identical, pristine testing environments on every developer machine.

## Why this matters
Test containers eliminate the 'works on my machine' syndrome for database and queue integration tests.

## First principles
Test Suite Starts -> Docker starts fresh Postgres container -> Run Migrations -> Execute Tests -> Container Destroyed.

## Mental model
```text
Docker Run postgres:16-alpine (Ephemeral Port) -> Apply Schema -> Run Integration Tests -> Docker Stop & Remove
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Testcontainers-python library integration with Pytest.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/101-test-containers-disposable-dependencies/tests/ -v
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
- **Failure Injection**: Spin up an ephemeral database container, apply migrations, run test suite, and tear down container cleanly.
- Execute the experiment script:
```bash
python phases/101-test-containers-disposable-dependencies/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify test suite passes identically on local macOS and Linux CI environments.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Reuse container instances across test runs in local development to save container startup overhead.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never connect automated test suites to external cloud databases that can be accessed by multiple developers simultaneously.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Disposable dependencies allow testing real failure modes: simulate network partitions by stopping containers midway.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What problem arises when multiple developers or CI jobs run tests against a shared, persistent database?
2. How do ephemeral test containers guarantee reproducibility across different developer workstations?
3. What are the speed tradeoffs of using test containers and how can container reuse optimize local testing?

## What comes next
Having understood test containers / disposable dependencies, we next discover its inherent boundaries and transition to **Property and Edge-Case Testing**.
