# Solution: Broken Pipeline Lab 18 — Persistent Self-Hosted Runner Leaves State from Previous Build

## 1. Root Cause Analysis
Self-hosted runner reused disk workspace without cleaning untracked files or stopping background daemon processes.

---

## 2. Step-by-Step Fix
Run ephemeral runners (e.g. Actions Runner Controller on Kubernetes) destroyed after each job, or run `git clean -ffdx` before and after every run.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/18-dirty-self-hosted-runner-state-leak/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Mandate ephemeral single-use runners for production CI workloads.
