# Lesson 154: Canary / Gradual Rollout Concepts

> **Motto**: Canary deployments route a small percentage of real production traffic to a new version, monitoring telemetry before wider release.

---

## Motto
"Canary deployments route a small percentage of real production traffic to a new version, monitoring telemetry before wider release."

## Problem
Deploying a new version to 100% of servers at once exposes all users to potential catastrophic outages.

## Prediction
Routing 2% of traffic to a canary instance verifies CPU, memory, and error rates against real user traffic safely.

## Why this matters
Canary releases catch subtle production bugs that never appear in staging or automated test suites.

## First principles
Traffic Split: 98% to Stable Baseline (v1.0) | 2% to Canary Instance (v1.1). Compare RED metrics between pools.

## Mental model
```text
Load Balancer ──┬──[98% Traffic]──> Production Baseline (v1.0) [Monitors 5xx: 0.01%]
                 └──[ 2% Traffic]──> Canary Pod (v1.1)           [Monitors 5xx: 0.01% -> SAFE TO ROLL OUT]
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Kubernetes / Istio / AWS ALB canary traffic routing.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/154-canary-gradual-rollout-concepts/tests/ -v
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
- **Failure Injection**: Simulate a canary deployment where v1.1 contains a subtle memory leak; compare metrics between baseline and canary.
- Execute the experiment script:
```bash
python phases/154-canary-gradual-rollout-concepts/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Automated canary analyzer detects elevated error rate on canary instance and aborts rollout, reverting traffic to v1.0.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Canary analysis requires statistical significance: do not evaluate canaries on tiny sample sizes (< 1,000 requests).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Monitor key RED metrics: if Canary Error Rate > Baseline Error Rate by 1%, trigger automated rollback.
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: Database migrations must support both baseline and canary versions simultaneously (Expand-Contract).
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. Where does the term 'canary deployment' originate and what does it mean in backend engineering?
2. What specific metrics should an automated canary analysis engine compare between baseline and canary pools?
3. Why must database schemas support both the baseline and canary software versions simultaneously?

## What comes next
Having understood canary / gradual rollout concepts, we next discover its inherent boundaries and transition to **Error Budgets / Reliability**.
