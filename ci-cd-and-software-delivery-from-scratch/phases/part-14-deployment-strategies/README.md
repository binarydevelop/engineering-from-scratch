# Part XIV: Deployment Strategies (Phases 97–103)

## Motto
> "Every deployment strategy is a conscious trade-off between infrastructure cost, rollback speed, state compatibility, and blast radius."

---

## Delivery Problem
An engineering team deploys a breaking change via Recreate deployment on a production payment gateway. The service experiences 6 minutes of total downtime, dropping 4,200 checkout transactions and triggering customer escalations.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 97–103 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
Recreate causes downtime. Rolling updates maintain capacity but require dual-version database compatibility. Blue/Green doubles capacity cost but offers instant rollback. Canary minimizes blast radius by testing real traffic incrementally.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
python3 deployment-labs/deploy_simulator.py --strategy rolling
echo "Exit Status: $?"
```

Observe the exact operating system signals, file mutations, and exit codes.

---

## Mental Model

```text
[ Source Input / State ]
           │
           ▼
[ Verification & Transformation Gate ]
           │
   ┌───────┴───────┐
   ▼               ▼
[ Pass: Exit 0 ]  [ Fail: Exit Non-Zero ]
   │               │
   ▼               ▼
[ Output State ]  [ Diagnostic Evidence ]
```

---

## Automate It
Encapsulate this manual process into deterministic scripts or platform workflows:
- Review companion implementations in `scripts/`, `pipelines/`, or lab directories.
- Ensure all automated steps run with `set -euo pipefail` and least-privilege permissions.

---

## Run It
Execute the automated test or runner command:

```bash
python3 deployment-labs/deploy_simulator.py --strategy rolling
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/27-canary-promoted-despite-elevated-5xx-errors/reproduce_failure.py
```

Observe the failure symptom, exit code, and error trace.

---

## Debug It
Follow the evidence-based troubleshooting loop:
1. What was the exact exit status?
2. Did standard error report missing dependencies, syntax rejections, or network timeouts?
3. What state did the failure leave behind?

---

## Security
- Enforce least privilege by default (`permissions: {}`).
- Protect production secrets using short-lived OIDC workload identity.
- Guard against untrusted fork PR exfiltration vectors.

---

## Optimize It
- Profile the critical path duration and remove redundant serial steps.
- Leverage intelligent caching with content-hashed keys.

---

## Deployment Implication
Connecting this stage to production software delivery protects customer-facing service level objectives (SLOs) and ensures that all deployed software is auditable and reversible.

---

## Recovery
If a defect bypasses this stage:
- Execute `./scripts/rollback.sh` to revert to the previous known-good immutable digest.
- Implement an automated regression check to ensure the defect cannot recur.

---

## Evidence
Record your verification proof:

```text
Part: 14
Date: 2026-09-27
Command Executed: python3 deployment-labs/deploy_simulator.py --strategy rolling
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XIV: Deployment Strategies (Phases 97–103))
1. **Exercise 14.1**: Run the deployment simulator in Recreate mode and observe the downtime interval.
2. **Exercise 14.2**: Execute a Rolling Update simulation with `maxSurge: 1` and `maxUnavailable: 0` and verify zero downtime.
3. **Exercise 14.3**: Simulate a Blue/Green router switch and measure the cutover duration in milliseconds.
4. **Exercise 14.4**: Execute a Canary rollout progression (1% -> 10% -> 50% -> 100%) and monitor error rates.
5. **Exercise 14.5**: Inject a 20% error rate into the canary and verify that automated abort cuts traffic immediately.
6. **Exercise 14.6**: Construct a comparative trade-off matrix evaluating cost, rollback speed, and state compatibility.
7. **Exercise 14.7**: Write a Prometheus PromQL query that calculates the error budget burn rate of a canary replica.
8. **Exercise 14.8**: Simulate state compatibility issues when v1 and v2 replicas concurrently access the same database.

---

## Questions for Mastery
1. *Deep architectural inquiry*: How does this stage balance feedback speed, financial compute cost, and deployment safety?
2. *Failure diagnosis inquiry*: If this step fails with an unexpected exit code, what log evidence reveals the root cause?
3. *First-principles inquiry*: Explain the core mechanism of this stage without referencing specific vendor brand names.

---

## When Not to Use This
Identify edge cases, architectures, or project scales where this technique is counterproductive or unnecessary overhead.

---

## What Comes Next
Proceed to the subsequent part to continue tracing the complete delivery path from Git commit to production software serving users.
