# Lesson 124: CI Basics

> **Motto**: Continuous Integration (CI) automatically builds, tests, and verifies every code commit in an isolated environment before merge.

---

## Motto
"Continuous Integration (CI) automatically builds, tests, and verifies every code commit in an isolated environment before merge."

## Problem
Merging code without automated CI verification allows broken syntax, failing tests, and security vulnerabilities into the main branch.

## Prediction
Configuring automated CI pipelines (GitHub Actions, GitLab CI) running linters, type checks, and tests guarantees code quality.

## Why this matters
CI provides fast, objective feedback on code quality, preventing broken builds from reaching staging or production.

## First principles
Git Push -> CI Trigger -> 1. Lint (Ruff) -> 2. Type Check (Mypy) -> 3. Run Pytest -> 4. Build Docker Image -> Pass/Fail.

## Mental model
```text
Developer Pushes Code ──> CI Pipeline (Lint -> Typecheck -> Test -> Security Scan) ──[PASS]──> Safe to Merge
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: GitHub Actions workflow manifests (`.github/workflows/ci.yml`).
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/124-ci-basics/tests/ -v
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
- **Failure Injection**: Trigger the CI test runner locally; assert that all linting, type-checking, and test steps execute and pass cleanly.
- Execute the experiment script:
```bash
python phases/124-ci-basics/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Introduce an intentional syntax error or failing test; verify that CI fails immediately and blocks deployment.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Keep CI pipelines fast (< 5 minutes): parallelize test suites and cache package dependencies to maintain developer velocity.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Run security dependency audits (`pip-audit` or `safety`) in CI to catch vulnerable packages before deployment.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Never allow merging pull requests to the main branch if the CI pipeline status is failing (Enforce Branch Protection).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the four primary stages of a robust backend Continuous Integration pipeline?
2. Why is CI pipeline execution speed (< 5 minutes) critical for engineering team productivity?
3. How do branch protection rules and CI status checks prevent broken code from entering production?

## What comes next
Having understood ci basics, we next discover its inherent boundaries and transition to **Deployment Environments**.
