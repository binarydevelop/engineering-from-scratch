# Solution: Broken Pipeline Lab 14 — Verbose Bash Debugging Prints Cloud Token to Public Log

## 1. Root Cause Analysis
Debugging flag `set -x` echoed environment variables and curl commands containing authorization headers.

---

## 2. Step-by-Step Fix
Never run `set -x` in scripts handling secrets; ensure CI runner secret masking is active and rotate exposed credential immediately.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/14-secret-printed-to-pipeline-logs/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Run automated log scanners in PR pipelines to block unmasked secrets.
