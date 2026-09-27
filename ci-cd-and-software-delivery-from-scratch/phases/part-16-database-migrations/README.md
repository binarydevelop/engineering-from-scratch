# Part XVI: Database Migrations in Delivery (Phases 108–113)

## Motto
> "Never execute breaking schema changes and code deployments simultaneously. Expand, Migrate, Contract is the foundation of zero-downtime persistence."

---

## Delivery Problem
A developer renames column `user_email` to `email` in a single migration script and deploys the new code. During the 15-minute rolling update, running v1 pods query `user_email` and crash because the column was renamed, causing an immediate production outage.

---

## Prediction
1. Adopting this engineering stage prevents common delivery failure modes before deployment.
2. Automating verified manual commands reduces lead time and eliminates human execution errors.
3. Establishing automated recovery runbooks ensures rapid Mean Time to Recovery (MTTR).

---

## Why This Matters
Software delivery is an end-to-end control system. Understanding Phases 108–113 ensures that your delivery system remains auditable, deterministic, secure, and observable from source commit to production runtime.

---

## First Principles
Database migrations must be backward-compatible with N-1 application versions. In the Expand phase, add new columns with defaults. In the Migrate phase, backfill data. In the Contract phase, drop legacy columns only after old code is completely decommissioned.

---

## Manual Process
Execute the underlying manual commands in your terminal before inspecting automated workflows:

```bash
# Execute the manual baseline
python3 sample-apps/delivery-service/db/migration_engine.py
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
python3 sample-apps/delivery-service/db/migration_engine.py
```

---

## Break It
Deliberately reproduce a realistic delivery failure:

```bash
python3 broken-pipelines/21-breaking-database-column-drop-instant-crash/reproduce_failure.py
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
Part: 16
Date: 2026-09-27
Command Executed: python3 sample-apps/delivery-service/db/migration_engine.py
Exit Code: 0
Verification Verified: Yes
```

---

## Practical Exercises (Part XVI: Database Migrations in Delivery (Phases 108–113))
1. **Exercise 16.1**: Run all 4 stages of migrations in `sample-apps/delivery-service/db/` and verify idempotency.
2. **Exercise 16.2**: Simulate an un-indexed table update on 100,000 rows and observe table lock starvation.
3. **Exercise 16.3**: Implement a batching backfill script that migrates records in chunks of 1,000 rows with sleep pauses.
4. **Exercise 16.4**: Write a SQL linter that detects and blocks `DROP COLUMN` and `ALTER COLUMN TYPE` in PR pipelines.
5. **Exercise 16.5**: Test simultaneous execution of v1 and v2 application code against the expanded schema.
6. **Exercise 16.6**: Simulate a migration failure midway through execution and test transactional rollback.
7. **Exercise 16.7**: Verify that `schema_migrations` records applied versions deterministically.
8. **Exercise 16.8**: Design a two-week migration release schedule across Expand, Migrate, and Contract phases.

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
