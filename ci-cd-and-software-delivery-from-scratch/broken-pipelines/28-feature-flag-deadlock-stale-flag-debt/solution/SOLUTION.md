# Solution: Broken Pipeline Lab 28 — Stale Feature Flag Code Path Causes Production Deadlock

## 1. Root Cause Analysis
The team treated feature flags as permanent configuration instead of temporary rollout mechanisms.

---

## 2. Step-by-Step Fix
Remove legacy flag code branch and make current behavior permanent.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/28-feature-flag-deadlock-stale-flag-debt/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Track flag age and establish a mandatory 30-day flag removal SLA.
