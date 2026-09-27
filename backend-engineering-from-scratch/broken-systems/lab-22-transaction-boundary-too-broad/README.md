# Broken Backend Lab: Connection Starvation from Mega-Transaction

> **Category**: Database  
> **Symptom**: Database connection pool exhausted under 10 concurrent requests; all queries blocked.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Database connection pool exhausted under 10 concurrent requests; all queries blocked.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Trace transaction start and commit times; identify 3-second external API call inside transaction.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Scope transaction strictly around SQL writes; move external network calls outside transaction.
- **Verification**: Run `pytest test_reproduce.py -v`.
