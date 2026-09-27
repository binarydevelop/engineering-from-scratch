# Broken Backend Lab: Silent Data Corruption from Swallowed Exception

> **Category**: Observability  
> **Symptom**: Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Inventory balance is wrong, but zero errors appear in logs or monitoring dashboards.
```

## 2. Architecture & Context
This subsystem handles critical observability operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Audit error handling; locate `except Exception: pass` swallowing integrity errors.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Remove blanket try-except; log error with full traceback and return structured 500 response.
- **Verification**: Run `pytest test_reproduce.py -v`.
