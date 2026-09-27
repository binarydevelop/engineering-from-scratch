# Broken Backend Lab: HTTP 500 Unhandled Null Reference

> **Category**: Validation  
> **Symptom**: Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Incoming JSON payload with missing optional nested field causes unhandled KeyError / AttributeError.
```

## 2. Architecture & Context
This subsystem handles critical validation operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect structured error log traceback and isolate missing field access in request handler.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Use strict Pydantic model with default values or safe `.get()` dictionary access.
- **Verification**: Run `pytest test_reproduce.py -v`.
