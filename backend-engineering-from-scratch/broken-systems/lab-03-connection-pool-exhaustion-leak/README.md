# Broken Backend Lab: Database Connection Pool Exhaustion Leak

> **Category**: Database  
> **Symptom**: All database connections become saturated; application hangs and times out after 10 requests.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
All database connections become saturated; application hangs and times out after 10 requests.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect pool checked-out connection count; identify missing finally/context manager in error path.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Wrap connection checkout in Python context managers (`with pool.acquire():`).
- **Verification**: Run `pytest test_reproduce.py -v`.
