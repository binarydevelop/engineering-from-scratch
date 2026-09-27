# Solution: Broken Pipeline Lab 25 — GitOps Controller Faithfully Deploys Broken Config Commit

## 1. Root Cause Analysis
Automation faithfully applying a bad desired state is still an outage. The config repo lacked pre-merge manifest validation.

---

## 2. Step-by-Step Fix
Revert the Git commit to restore prior good desired state.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/25-gitops-reconciler-deploys-bad-desired-state/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Run automated linters (`kubeconform`, `kustomize build`) on PRs to the GitOps configuration repo before merge.
