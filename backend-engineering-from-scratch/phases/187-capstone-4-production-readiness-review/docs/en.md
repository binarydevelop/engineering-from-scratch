# Lesson 187: Capstone 4: Production Readiness Review

> **Motto**: Perform a rigorous architectural and operational audit of Capstone 1 against the complete production readiness checklist.

---

## Motto
"Perform a rigorous architectural and operational audit of Capstone 1 against the complete production readiness checklist."

## Problem
Deploying to production without a structured readiness review leads to preventable launch-day disasters.

## Prediction
Auditing security, connection pools, timeouts, observability, graceful shutdown, and migrations ensures enterprise reliability.

## Why this matters
This capstone generates an authoritative, actionable Production Readiness Review document approving deployment.

## First principles
Audit Dimensions: Security & Auth, Persistence & Pooling, Resilience & Timeouts, Observability, Deployment & Containers.

## Mental model
```text
Capstone Architecture ──[Audit against Production Checklist]──> Actionable Findings -> Remediations -> Production Sign-Off
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Production readiness review audit and verification report.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/187-capstone-4-production-readiness-review/tests/ -v
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
- **Failure Injection**: Execute the automated readiness audit against Capstone 1; review findings across all 7 operational categories.
- Execute the experiment script:
```bash
python phases/187-capstone-4-production-readiness-review/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Verify 100% compliance: confirm health endpoints, timeouts, connection limits, graceful shutdown, and secret hygiene.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: A production readiness review is not a formality: any failed critical item must block production deployment.
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Document actionable runbooks for common alerts (database pool exhaustion, elevated 5xx rates, worker lag).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Review cost and resource sizing: verify container CPU and memory limits are configured appropriately.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What are the seven operational categories evaluated in the Capstone 4 Production Readiness Review?
2. What critical vulnerabilities would prevent an engineering director from signing off on a production deployment?
3. How does conducting a formal readiness review reduce mean time to recovery (MTTR) during real production incidents?

## What comes next
Having understood capstone 4: production readiness review, we next discover its inherent boundaries and transition to **Backend in System Design**.
