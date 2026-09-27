# Broken Backend Lab: Circuit Breaker Permanently Stuck in Open State

> **Category**: Reliability  
> **Symptom**: Downstream service recovers, but circuit breaker continues failing fast and never probes.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Downstream service recovers, but circuit breaker continues failing fast and never probes.
```

## 2. Architecture & Context
This subsystem handles critical reliability operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect circuit breaker state machine transitions; observe half-open timer never fires.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Implement reset timeout logic allowing trial probe requests in HALF-OPEN state.
- **Verification**: Run `pytest test_reproduce.py -v`.
