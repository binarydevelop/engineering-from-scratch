# Broken Pipeline Lab 09: Embedded Wall-Clock Timestamp Prevents Build Reproducibility

**Category:** Build
**Target Failure:** Rebuilding the exact same commit SHA produces a different SHA-256 binary hash, breaking artifact verification and caching.

---

## 1. Incident Scenario & Symptoms
A pull request or production deployment pipeline was triggered. Rather than succeeding, the run terminated with the following operational failure:

> "Rebuilding the exact same commit SHA produces a different SHA-256 binary hash, breaking artifact verification and caching."

Your task is to diagnose the root cause, identify what evidence exists in the pipeline logs and runner state, and implement a durable fix.

---

## 2. Reproduction Command
Execute the broken reproduction script from the repository root:

```bash
python3 broken-pipelines/09-non-deterministic-timestamp-in-build/reproduce_failure.py
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
