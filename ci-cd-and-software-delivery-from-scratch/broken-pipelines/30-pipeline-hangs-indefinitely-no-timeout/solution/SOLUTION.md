# Solution: Broken Pipeline Lab 30 — Interactive Prompt Hangs CI Runner For 6 Hours

## 1. Root Cause Analysis
Step lacked non-interactive flags and the workflow had no job-level timeout configured.

---

## 2. Step-by-Step Fix
Pass non-interactive flags (`-y`, `--no-input`) and configure explicit job timeout (`timeout-minutes: 15`).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/30-pipeline-hangs-indefinitely-no-timeout/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Mandate default timeouts on all platform pipeline templates.
