# Broken Backend Lab: Dropped Requests During Rolling Container Deploy

> **Category**: Deployment  
> **Symptom**: Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Kubernetes rolling update causes 502 Bad Gateway errors for in-flight requests.
```

## 2. Architecture & Context
This subsystem handles critical deployment operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect container shutdown logs; observe process terminates instantly on SIGTERM without waiting.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Implement graceful shutdown intercepting SIGTERM and allowing active requests 15s to complete.
- **Verification**: Run `pytest test_reproduce.py -v`.
