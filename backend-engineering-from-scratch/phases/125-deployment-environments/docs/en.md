# Lesson 125: Deployment Environments

> **Motto**: Separating deployment environments (Dev, Test, Staging, Production) isolates experimental code from real user data.

---

## Motto
"Separating deployment environments (Dev, Test, Staging, Production) isolates experimental code from real user data."

## Problem
Testing new features directly against production databases risks data corruption, accidental emails, and user downtime.

## Prediction
Promoting immutable artifacts through Dev -> Test -> Staging -> Prod ensures features are tested in identical conditions.

## Why this matters
Environment separation protects production confidentiality, integrity, and availability.

## First principles
Development (Local experiments) -> Staging (Pre-production replica) -> Production (Live customer traffic).

## Mental model
```text
Code Commit -> Dev Environment -> CI Tests -> Staging Deploy (Smoke Tests) -> Production Promotion
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: 12-factor environment configuration in multi-stage deployment pipelines.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/125-deployment-environments/tests/ -v
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
- **Failure Injection**: Attempt to run a destructive database drop script while `APP_ENV=production`; verify safety guard aborts instantly.
- Execute the experiment script:
```bash
python phases/125-deployment-environments/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify that development environment enables debug docs while production environment disables debug docs and enforces HTTPS.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Staging environments should mirror production hardware, networking, and configuration as closely as possible (Parity).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Never use real production user data in development or staging environments; sanitize or generate synthetic datasets.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: The exact same container image artifact built in CI must be promoted through staging to production without rebuilding.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Why must the exact same container image artifact be promoted across environments without rebuilding?
2. What safety guards should be placed on destructive database scripts to prevent running in production?
3. Why is using real production user data in staging environments a severe security and privacy violation?

## What comes next
Having understood deployment environments, we next discover its inherent boundaries and transition to **Production Readiness**.
