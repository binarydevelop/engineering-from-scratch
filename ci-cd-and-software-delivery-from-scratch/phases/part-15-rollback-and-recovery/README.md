# Part XV: Rollback & Recovery (Phases 104–107)

## Motto
> "Never assume rollback is guaranteed. A recovery plan that has never been tested in production is mere wishful thinking."

---

## Delivery Problem
A bug in release v2 causes data corruption. The on-call engineer rolls back the application image to v1. However, v2 ran a migration that dropped a column required by v1. Re-deploying v1 crashes instantly, leaving the team with both versions broken.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 104–107 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
Application rollback is independent of database rollback. When irreversible data transformations occur, roll-forward (deploying v3 with a fix) is often safer than rolling back.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
bash scripts/rollback.sh staging prev-known-good
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
bash scripts/rollback.sh staging prev-known-good
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/22-rollback-fails-due-to-irreversible-migration/reproduce_failure.py
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
Part: 15
Date: 2026-09-27
Command Executed: bash scripts/rollback.sh staging prev-known-good
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XV: Rollback & Recovery (Phases 104–107))
1. **Exercise 15.1**: Execute `scripts/rollback.sh` and inspect the pre-flight database schema compatibility check.
2. **Exercise 15.2**: Simulate an irreversible schema change and observe why application rollback fails.
3. **Exercise 15.3**: Measure Mean Time to Recovery (MTTR) across 5 simulated rollback exercises.
4. **Exercise 15.4**: Formulate a decision matrix for when to Roll Back vs when to Roll Forward.
5. **Exercise 15.5**: Write an automated rollback hook in GitHub Actions that executes on step failure.
6. **Exercise 15.6**: Test reverting a Git commit in a GitOps configuration repository to trigger automated recovery.
7. **Exercise 15.7**: Design an emergency hotfix workflow that bypasses non-critical linters while maintaining security checks.
8. **Exercise 15.8**: Document a post-incident recovery runbook for a failed database migration.

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
