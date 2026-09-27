# Broken Backend Lab: Insecure Wildcard CORS Configuration

> **Category**: Security  
> **Symptom**: Browser blocks request or allows unauthorized origins to read sensitive authenticated data.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Browser blocks request or allows unauthorized origins to read sensitive authenticated data.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect preflight `Access-Control-Allow-Origin` and `Access-Control-Allow-Credentials` headers.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Replace wildcard origin with an explicit whitelist of trusted frontend domains.
- **Verification**: Run `pytest test_reproduce.py -v`.
