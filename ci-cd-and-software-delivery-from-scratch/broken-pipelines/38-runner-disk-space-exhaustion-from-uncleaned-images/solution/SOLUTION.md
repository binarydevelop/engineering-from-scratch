# Solution: Broken Pipeline Lab 38 — Self-Hosted Runner Fails with 'No space left on device'

## 1. Root Cause Analysis
Months of dangling Docker images and temporary build caches accumulated on persistent runner disk.

---

## 2. Step-by-Step Fix
Run automated disk cleanup: `docker system prune -af --filter 'until=48h'`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/38-runner-disk-space-exhaustion-from-uncleaned-images/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Configure automated cron maintenance or switch to ephemeral auto-scaling runners.
