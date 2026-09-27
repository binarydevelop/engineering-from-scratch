# Solution: Broken Pipeline Lab 27 — Canary Rollout Metric Threshold Too Lenient, Promoting Buggy Code

## 1. Root Cause Analysis
Health analysis evaluated absolute success count instead of error percentage / failure ratio.

---

## 2. Step-by-Step Fix
Define strict error rate SLO guardrail (e.g. error rate must not exceed 0.5% during canary window).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/27-canary-promoted-despite-elevated-5xx-errors/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Implement automated abort triggers that halt and revert canary immediately upon error budget burn.
