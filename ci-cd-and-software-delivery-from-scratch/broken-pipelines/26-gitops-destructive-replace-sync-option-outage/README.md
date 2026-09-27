# Broken Pipeline Lab 26: Argo CD Replace Sync Option Deletes Running Resources

**Category:** GitOps
**Target Failure:** Enabling `--replace` in sync options deletes active Deployment pods, causing an outage instead of a rolling update.

---

## 1. Incident Scenario & Symptoms
A pull request or production deployment pipeline was triggered. Rather than succeeding, the run terminated with the following operational failure:

> "Enabling `--replace` in sync options deletes active Deployment pods, causing an outage instead of a rolling update."

Your task is to diagnose the root cause, identify what evidence exists in the pipeline logs and runner state, and implement a durable fix.

---

## 2. Reproduction Command
Execute the broken reproduction script from the repository root:

```bash
python3 broken-pipelines/26-gitops-destructive-replace-sync-option-outage/reproduce_failure.py
```

Observe the non-zero exit code, error traces, and system side effects.

---

## 3. Diagnostic Inquiries
Before checking the solution, answer these guided diagnostic questions:
1. *Trigger & Context*: Which exact stage or tool emitted the failure?
2. *Identity*: Did the failure occur before or after artifact creation?
3. *Transient vs Deterministic*: If you rerun this command 5 times, will it ever pass? Why or why not?
4. *Blast Radius*: If this pipeline had completed silently, what production impact would have occurred?

---

## 4. Finding the Solution
The verified fix and engineering post-mortem are available in:
[`solution/SOLUTION.md`](solution/SOLUTION.md)
