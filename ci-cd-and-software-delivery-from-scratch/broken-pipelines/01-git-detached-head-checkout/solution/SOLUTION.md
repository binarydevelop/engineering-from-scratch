# Solution: Broken Pipeline Lab 01 — Detached HEAD Commit Never Pushed or Tracked

## 1. Root Cause Analysis
CI runners frequently checkout specific commit SHAs directly (`git checkout <SHA>`) which leaves HEAD detached. Scripts assuming an active branch cannot push or resolve tracking refs.

---

## 2. Step-by-Step Fix
Use explicit branch checkout or create an ephemeral tracking branch: `git checkout -b temp-branch <SHA>` or pass full ref names to push commands.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/01-git-detached-head-checkout/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Never rely on branch state inside containerized CI runners. Explicitly specify source ref and destination ref in git operations.
