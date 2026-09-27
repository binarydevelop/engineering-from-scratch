# Broken Pipeline Lab 08: Circular Dependency in Build Graph Halts Pipeline

**Category:** Build
**Target Failure:** Build tool hangs indefinitely or crashes with `RecursionError: cyclic dependency detected between target A and target B`.

---

## 1. Incident Scenario & Symptoms
A pull request or production deployment pipeline was triggered. Rather than succeeding, the run terminated with the following operational failure:

> "Build tool hangs indefinitely or crashes with `RecursionError: cyclic dependency detected between target A and target B`."

Your task is to diagnose the root cause, identify what evidence exists in the pipeline logs and runner state, and implement a durable fix.

---

## 2. Reproduction Command
Execute the broken reproduction script from the repository root:

```bash
python3 broken-pipelines/08-build-dag-circular-dependency/reproduce_failure.py
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
