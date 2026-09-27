# Solution: Broken Pipeline Lab 12 — Container Registry Throttling Causes Pipeline Retry Storm

## 1. Root Cause Analysis
Hundreds of parallel CI workers hit the external registry simultaneously without layer caching or exponential backoff.

---

## 2. Step-by-Step Fix
Implement registry pull-through cache and add jittered exponential backoff on transient registry failures.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/12-registry-outage-retry-storm/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Host a local registry mirror and use local layer caching.
