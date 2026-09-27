# Broken Backend Lab: Stale Data Returned Due to Missing Cache Eviction

> **Category**: Caching  
> **Symptom**: Database contains updated product price, but API GET endpoint returns old price indefinitely.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Database contains updated product price, but API GET endpoint returns old price indefinitely.
```

## 2. Architecture & Context
This subsystem handles critical caching operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Compare database row with Redis key; audit update route for missing `cache.delete()`.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Add post-commit cache eviction hook on all state-mutating endpoints.
- **Verification**: Run `pytest test_reproduce.py -v`.
