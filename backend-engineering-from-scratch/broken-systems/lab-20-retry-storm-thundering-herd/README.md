# Broken Backend Lab: Retry Storm Crashing Recovering Database

> **Category**: Reliability  
> **Symptom**: When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
When database recovers from brief hiccup, 500 clients retry simultaneously, immediately crashing it again.
```

## 2. Architecture & Context
This subsystem handles critical reliability operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect traffic arrival graph; observe synchronized retry spikes every 5 seconds.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Add exponential backoff with Full Jitter to decorrelate client retries.
- **Verification**: Run `pytest test_reproduce.py -v`.
