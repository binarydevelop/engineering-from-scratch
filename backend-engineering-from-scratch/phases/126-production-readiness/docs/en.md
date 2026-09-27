# Lesson 126: Production Readiness

> **Motto**: Production readiness audits a backend system across reliability, security, observability, and operability before release.

---

## Motto
"Production readiness audits a backend system across reliability, security, observability, and operability before release."

## Problem
Deploying a service that only works under happy-path conditions guarantees an emergency outage during the first traffic surge.

## Prediction
Evaluating systems against the comprehensive Production Readiness Checklist identifies hidden operational failure modes.

## Why this matters
Production readiness reviews turn hopeful releases into calm, predictable, and resilient operations.

## First principles
Audit Pillars: 1. Health Checks, 2. Timeouts/Retries, 3. Pool Limits, 4. Auth/Security, 5. Metrics/Logs, 6. Graceful Shutdown.

## Mental model
```text
Service Assessment ──[Production Checklist Audit]──> Identify Gaps -> Remediate Vulnerabilities -> Approved for Release
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Production readiness review documentation and sign-off processes.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/126-production-readiness/tests/ -v
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
- **Failure Injection**: Run the readiness auditor against an unhardened service; observe it flags missing timeouts, unbound pools, and missing health endpoints.
- Execute the experiment script:
```bash
python phases/126-production-readiness/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Remediate all flagged items; re-run auditor; assert service achieves 100% compliance score.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: A single unchecked item on the production readiness checklist can cause a total system outage under real-world load.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Production readiness is an engineering habit: ask the hard questions about failures before your customers experience them.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Maintain a living production checklist updated with lessons learned from every post-mortem incident review.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the six foundational pillars of a Backend Production Readiness Review?
2. Why is a service that passes 100% of its unit tests NOT necessarily ready for production deployment?
3. How does conducting production readiness reviews prevent recurring on-call outages?

## What comes next
Having understood production readiness, we next discover its inherent boundaries and transition to **Security Headers / HTTPS**.
