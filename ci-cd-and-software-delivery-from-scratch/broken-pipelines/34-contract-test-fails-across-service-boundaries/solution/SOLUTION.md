# Solution: Broken Pipeline Lab 34 — Service A Drops Field Required by Service B Consumer Contract

## 1. Root Cause Analysis
Service A removed an 'unused' response field without validating consumer-driven contracts.

---

## 2. Step-by-Step Fix
Restore the field or introduce versioned API endpoint `/v2/orders`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/34-contract-test-fails-across-service-boundaries/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Run contract tests against consumer contract specifications in CI before merging PRs.
