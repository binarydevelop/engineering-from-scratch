# Lesson 155: Error Budgets / Reliability

> **Motto**: Reliability is a product requirement; Service Level Objectives (SLOs) and Error Budgets balance shipping speed with stability.

---

## Motto
"Reliability is a product requirement; Service Level Objectives (SLOs) and Error Budgets balance shipping speed with stability."

## Problem
Demanding 100% uptime is mathematically impossible and economically irrational; 99.9% availability allows an error budget.

## Prediction
An Error Budget defines the acceptable room for failure (e.g. 0.1% = 43 minutes of downtime/month), governing release velocity.

## Why this matters
Error budgets eliminate developer vs SRE friction: if budget remains, ship fast; if budget exhausts, halt features and fix reliability.

## First principles
SLA (Contractual promise to customers) -> SLO (Internal target, e.g. 99.9%) -> SLI (Actual measured availability).

## Mental model
```text
SLO Target: 99.9% Availability. Error Budget = 100% - 99.9% = 0.1% allowable failed requests.
```

## Build the simple version
Review the core implementation in `code/main.py`. This mechanism builds the underlying abstraction from first principles using Python standard library primitives:
```python
# Refer to code/main.py for the runnable implementation
```

## Use the real tool/framework
How modern production frameworks and tools handle this layer:
- **Framework Abstraction**: Prometheus SLO alerting rules using Multi-Window Multi-Burn-Rate alerts.
- Notice that the framework provides ergonomics and performance optimizations, but the underlying protocol and operating system invariants remain identical to our from-scratch implementation.

## Test it
Run the verification suite:
```bash
pytest phases/155-error-budgets-reliability-thinking/tests/ -v
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
- **Failure Injection**: Simulate an incident consuming 20% of monthly error budget in 10 minutes; calculate burn rate.
- Execute the experiment script:
```bash
python phases/155-error-budgets-reliability-thinking/experiments/run_experiment.py
```

## Debug it
Isolate the failing layer without guessing:
- **Diagnostic Method**: Error budget monitor triggers 'High Burn Rate' alert and recommends freezing non-critical feature releases.
- Trace request correlation IDs across application logs and exception stack traces

## Improve it
Apply defensive engineering to eliminate the vulnerability or bottleneck:
- **Defensive Refactoring**: Three nines (99.9%) = 43.8 minutes downtime/month. Four nines (99.99%) = 4.38 minutes downtime/month (10x cost).
- Enforce strict bounds, transactions, and fallback behaviors

## Security
Analyze the security boundary for this layer:
- **Threat Model**: Measure SLIs from the customer perspective (e.g. percentage of successful user requests at the API Gateway).
- Ensure principle of least privilege, input sanitization, and defense-in-depth

## Production implications
How this manifests in production infrastructure:
- **Production Operations**: When the error budget is exhausted, team policy must mandate prioritizing stability and bug fixes over new features.
- Monitor RED telemetry signals and configure alert thresholds for SLO compliance

## Evidence
Record your empirical observations in `outputs/evidence-template.md`.

## Questions for mastery
1. What is the mathematical relationship between an SLI, an SLO, and an Error Budget?
2. How much total downtime per month is permitted by a 99.9% availability SLO versus a 99.99% SLO?
3. How does an exhausted error budget resolve tension between developer feature velocity and SRE stability?

## What comes next
Having understood error budgets / reliability, we next discover its inherent boundaries and transition to **Capacity Estimation**.
