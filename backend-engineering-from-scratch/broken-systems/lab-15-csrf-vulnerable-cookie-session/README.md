# Broken Backend Lab: Cross-Site Request Forgery on State Mutation

> **Category**: Security  
> **Symptom**: Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Rogue third-party website triggers unauthorized money transfer using victim's cached cookie.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect POST request headers; identify missing CSRF anti-forgery token verification.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Require cryptographic anti-CSRF token verification and enforce `SameSite=Lax` on cookies.
- **Verification**: Run `pytest test_reproduce.py -v`.
