# Solution: Broken Pipeline Lab 15 — Malicious Fork PR Leverages pull_request_target to Read Secrets

## 1. Root Cause Analysis
Workflow triggered on `pull_request_target` and checked out untrusted PR head commit while retaining secret access.

---

## 2. Step-by-Step Fix
Trigger untrusted PRs on `pull_request` (no secrets), or never checkout PR head in `pull_request_target`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/15-fork-pr-exfiltrating-ci-secret/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Enforce strict separation between untrusted PR validation and privileged release workflows.
