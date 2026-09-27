# Solution: Broken Pipeline Lab 16 — CI Token Holds Full Cloud Administrator Privileges

## 1. Root Cause Analysis
CI runner was assigned an IAM role with `AdministratorAccess` instead of narrow role scoped to specific registry/bucket.

---

## 2. Step-by-Step Fix
Apply least privilege IAM policy allowing only `ecr:PutImage` and `s3:PutObject` for specific artifact paths.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/16-overprivileged-ci-runner-token/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Audit CI IAM roles quarterly and mandate role scoping per workflow.
