# Solution: Broken Pipeline Lab 26 — Argo CD Replace Sync Option Deletes Running Resources

## 1. Root Cause Analysis
The `--replace` or `--force` flag bypasses normal Kubernetes rolling updates and deletes the existing object.

---

## 2. Step-by-Step Fix
Remove `--replace` from Argo CD sync options and rely on standard `kubectl apply` declarative updates.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/26-gitops-destructive-replace-sync-option-outage/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Flag and reject dangerous Argo CD sync flags in organizational policy engine.
