# Phase 83: Failure Day

## Motto
> Never fear failure. Induce it, observe it, diagnose it, recover it, and explain it.

**Type:** Chaos Engineering & Disaster Lab  
**Time Estimate:** ~90 minutes  
**Prerequisites:** Phase 82: Production-Like AWS Capstone  
**AWS Services Involved:** Chaos Engineering, Fault Injection, Diagnostic Flowcharts  
**Cost Vector:** Failure Day simulation runs locally at zero cost ($0.00).  

---

## Problem
Engineers panic during production outages because they have never experienced systems failure in a controlled environment.

---

## Prediction
Intentionally injecting failures (killing compute, denying IAM permissions, severing security groups, blackholing routes) builds muscle memory and diagnostic mastery.

---

## Why this matters
A systems engineer is forged during outages. Failure Day turns abstract theory into concrete diagnostic confidence.

---

## First principles
The 6-Step Chaos Protocol: (1) **Predict**: Formulate explicit hypothesis of expected symptom. (2) **Break**: Intentionally inject failure. (3) **Observe**: Read raw telemetry, error codes, and packet drops. (4) **Diagnose**: Follow systematic diagnostic tree. (5) **Recover**: Execute remediation action. (6) **Explain**: Derive the physical and protocol root cause.

---

## Mental model
```text
The Chaos Loop:
[ 1. PREDICT ] ──► [ 2. BREAK ] ──► [ 3. OBSERVE ]
                                          │
    ┌─────────────────────────────────────┘
    ▼
[ 4. DIAGNOSE ] ──► [ 5. RECOVER ] ──► [ 6. EXPLAIN FIRST PRINCIPLES ]
```

---

## Architecture before AWS
Unscheduled physical power cuts or pull-the-plug drills in enterprise datacenters.

---

## Build the primitive
```python
# Run our complete Phase 83 Failure Day chaos runner
import subprocess
subprocess.run(['python3', 'experiments/failure_day.py'], check=True)
```

---

## Use AWS
```bash
# Local chaos runner: python3 experiments/failure_day.py
```

---

## Inspect it
```bash
python3 experiments/failure_day.py
```

---

## Measure it
Measure Mean Time To Diagnose (MTTD) and Mean Time To Recovery (MTTR) across 7 chaos scenarios.

---

## Break it
Walk through all 7 chaos scenarios: Process crash, IAM revocation, SG severing, Poison pill, Route blackhole, Cache stampede, Unhealthy targets.

---

## Diagnose it
Follow the exact diagnostic decision trees in `docs/troubleshooting.md`.

---

## Recover it
Execute verified recovery commands for each scenario.

---

## Security
Never create dangerous public exposure (`0.0.0.0/0` on sensitive ports) as a failure exercise.

---

## Cost
### Cost Warning
Failure Day simulation runs locally at zero cost ($0.00).

### Resources Created
- Documented in lesson steps above.

### How to Verify Them
```bash
./scripts/list-lab-resources.sh
```

---

## Modify it
Experiment by tuning parameters, increasing capacity, changing timeouts, or tweaking security group rules. Observe metric changes in CloudWatch.

---

## Cleanup
```bash
# No resources created.
```

---

## Verify cleanup
```bash
echo 'Account clean.'
```

---

## Evidence
Record your laboratory findings using the mandatory evidence log template at `outputs/evidence-template.md`. Save your completed evidence log as `outputs/phase-83-evidence.md`.

---

## Questions for mastery
1. Why does a Security Group block cause 'Connection timed out' while an inactive service causes 'Connection refused'?
2. Why do IAM policy permission changes take effect within seconds without requiring a server reboot?
3. How does a Dead-Letter Queue prevent poison pill messages from causing infinite consumer crash loops?

---

## When to use this
Conduct Failure Day drills quarterly with engineering teams before launching major production updates.

---

## When not to use this
Never run chaos tests in production without automated rollback safeguards and on-call engineer awareness.

---

## What comes next
Phase 84: Architecture From Requirements — Deriving complete systems from business constraints.
