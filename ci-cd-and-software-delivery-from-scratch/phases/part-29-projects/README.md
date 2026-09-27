# Part XXIX: Substantial Projects (Phases 206–216)

## Motto
> "Synthesize first principles into working production delivery systems. Build complete runners, GitOps pipelines, OIDC authenticators, and provenance attestation suites."

---

## Delivery Problem
Engineers understand theoretical CI/CD concepts but struggle to design end-to-end architectures connecting source code to live production environments.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 206–216 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
Constructing working, end-to-end delivery projects builds visceral intuition. Each project tackles a specific architectural tier: local execution, cloud actions, containerization, staging, production, identity federation, supply-chain attestation, monorepos, and GitOps.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
python3 projects/setup_all_projects.py
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
python3 projects/setup_all_projects.py
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/verify_all_labs.py
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
Part: 29
Date: 2026-09-27
Command Executed: python3 projects/setup_all_projects.py
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XXIX: Substantial Projects (Phases 206–216))
1. **Exercise 29.1**: Complete Project 01: Build a Local CI Runner from scratch in Python.
2. **Exercise 29.2**: Complete Project 02: Full GitHub Actions CI pipeline with parallel jobs and sharding.
3. **Exercise 29.3**: Complete Project 03: Immutable container packaging and content-digest delivery.
4. **Exercise 29.4**: Complete Project 04: Automated staging deployment with smoke tests and contract checks.
5. **Exercise 29.5**: Complete Project 05: Production delivery pipeline with environment protections and rollback.
6. **Exercise 29.6**: Complete Project 06: OIDC short-lived workload identity federation without static secrets.
7. **Exercise 29.7**: Complete Project 07: Supply-chain SBOM and SLSA Provenance attestation suite.
8. **Exercise 29.8**: Complete Project 10: Declarative GitOps delivery with Argo CD reconciler.

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
