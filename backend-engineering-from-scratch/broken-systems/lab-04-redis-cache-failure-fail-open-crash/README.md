# Broken Backend Lab: Application Crash on Redis Cache Outage

> **Category**: Caching  
> **Symptom**: When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
When Redis crashes, entire API throws unhandled ConnectionRefusedError returning 500 for all reads.
```

## 2. Architecture & Context
This subsystem handles critical caching operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Check cache client error logs; observe unhandled exception bypassing database fallback.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Implement try-fallback block allowing cache read failures to fail open to primary database.
- **Verification**: Run `pytest test_reproduce.py -v`.
