# Part XXIII: GitOps & Declarative Delivery (Phases 153–165)

## Motto
> "Git is the single source of truth for desired state. An automated reconciler pulls changes and eliminates drift. Never use dangerous force-sync options in production."

---

## Delivery Problem
An engineer logs into the production Kubernetes cluster and manually runs `kubectl scale --replicas=10` during a spike. Days later, another engineer updates the deployment. The manual scaling is silently wiped out because the live cluster had drifted from Git.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 153–165 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
GitOps uses an in-cluster reconciler (Argo CD) to continuously compare Git desired state against live cluster state. Drift is detected and corrected automatically. Dangerous sync flags like `--replace` delete live resources and cause outages.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
python3 gitops/gitops_reconciler.py --mode status
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
python3 gitops/gitops_reconciler.py --mode status
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/26-gitops-destructive-replace-sync-option-outage/reproduce_failure.py
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
Part: 23
Date: 2026-09-27
Command Executed: python3 gitops/gitops_reconciler.py --mode status
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XXIII: GitOps & Declarative Delivery (Phases 153–165))
1. **Exercise 23.1**: Run `gitops/gitops_reconciler.py` in dry-run mode and inspect detected drift.
2. **Exercise 23.2**: Inject manual drift (`--replicas=10`) and observe how the reconciler detects `[OutOfSync]`.
3. **Exercise 23.3**: Execute automated reconciliation and verify transition back to `[Synced]` state.
4. **Exercise 23.4**: Simulate the hazardous `--replace` sync option and document why it destroys live pods.
5. **Exercise 23.5**: Compare the Application repository vs Configuration repository separation pattern.
6. **Exercise 23.6**: Execute a GitOps rollback by reverting a Git commit in the desired-state repository.
7. **Exercise 23.7**: Configure an automated drift alert notifying on-call engineers of unauthorized manual changes.
8. **Exercise 23.8**: Audit Kubernetes RBAC rules to ensure developers have read-only access while Argo CD reconciles.

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
