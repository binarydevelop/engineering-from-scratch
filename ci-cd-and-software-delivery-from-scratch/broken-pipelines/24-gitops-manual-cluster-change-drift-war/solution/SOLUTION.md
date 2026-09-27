# Solution: Broken Pipeline Lab 24 — Manual 'kubectl edit' Reverted in Endless Fight With Reconciler

## 1. Root Cause Analysis
The engineer updated the live cluster directly rather than committing the change to Git (desired state source of truth).

---

## 2. Step-by-Step Fix
Commit desired replica count to Git, or use horizontal pod autoscaling (HPA) so replica count is managed dynamically.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/24-gitops-manual-cluster-change-drift-war/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Configure production RBAC to deny direct manual edit access to human engineers.
