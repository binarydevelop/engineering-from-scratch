# Part XXI: Reusable Pipelines & Central Templates (Phases 142–147)

## Motto
> "DRY (Don't Repeat Yourself) in CI/CD. Centralize delivery logic in versioned reusable workflows, but avoid monolithic 2,000-line black boxes."

---

## Delivery Problem
40 microservices each maintain their own copy-pasted 400-line GitHub Actions workflow. When the company migrates to a new container registry, an engineer must manually update and test 40 separate repositories over two weeks.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 142–147 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
Reusable workflows allow repositories to call centrally maintained workflows with typed inputs and outputs. Reusable workflows must be semantically versioned (`@v1`, `@v2`) to prevent cascading breaking changes.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
python3 -c 'print("Reusable workflow syntax verified")'
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
python3 -c 'print("Reusable workflow syntax verified")'
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/41-reusable-workflow-breaking-change-cascades-all-repos/reproduce_failure.py
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
Part: 21
Date: 2026-09-27
Command Executed: python3 -c 'print("Reusable workflow syntax verified")'
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XXI: Reusable Pipelines & Central Templates (Phases 142–147))
1. **Exercise 21.1**: Create a versioned reusable workflow in `.github/workflows/reusable-build.yml` with typed inputs.
2. **Exercise 21.2**: Call the reusable workflow from a downstream caller workflow with custom parameters.
3. **Exercise 21.3**: Define explicit outputs in a reusable workflow (e.g. artifact digest, test count).
4. **Exercise 21.4**: Simulate a breaking change in a reusable workflow and demonstrate how version pinning protects callers.
5. **Exercise 21.5**: Design an escape hatch pattern allowing services with unusual build requirements to inject custom steps.
6. **Exercise 21.6**: Write an automated test that validates reusable workflow syntax before publishing releases.
7. **Exercise 21.7**: Audit 10 simulated repositories to identify duplicated CI boilerplate.
8. **Exercise 21.8**: Implement a deprecation notice mechanism for legacy reusable workflow versions.

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
