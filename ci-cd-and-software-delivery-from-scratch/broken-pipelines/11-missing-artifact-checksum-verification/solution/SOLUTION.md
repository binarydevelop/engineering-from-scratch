# Solution: Broken Pipeline Lab 11 — Corrupted or Tampered Artifact Deployed Without Hash Check

## 1. Root Cause Analysis
Deployment script downloaded artifact over network and executed it without verifying SHA-256 checksum against signed manifest.

---

## 2. Step-by-Step Fix
Always compute SHA-256 of downloaded artifacts and assert exact match before execution.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/11-missing-artifact-checksum-verification/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Integrate cryptographic checksum verification into deployment agents.
