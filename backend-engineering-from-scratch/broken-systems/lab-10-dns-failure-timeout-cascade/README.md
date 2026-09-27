# Broken Backend Lab: External Dependency Timeout Cascade

> **Category**: Network  
> **Symptom**: Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Third-party payment API hangs; upstream caller threads wait 60s, exhausting thread pools.
```

## 2. Architecture & Context
This subsystem handles critical network operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect active thread states; observe 50 threads blocked in socket read to third-party IP.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Configure strict socket connect timeout (2s), read timeout (5s), and circuit breaker.
- **Verification**: Run `pytest test_reproduce.py -v`.
