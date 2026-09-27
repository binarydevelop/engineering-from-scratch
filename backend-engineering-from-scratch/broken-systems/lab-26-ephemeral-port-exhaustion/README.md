# Broken Backend Lab: Socket Exhaustion from Connection Churn

> **Category**: Network  
> **Symptom**: High-throughput API throws `OSError: [Errno 99] Cannot assign requested address`.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
High-throughput API throws `OSError: [Errno 99] Cannot assign requested address`.
```

## 2. Architecture & Context
This subsystem handles critical network operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect socket states with `ss -tan`; observe 30,000 sockets in `TIME_WAIT` state.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Use persistent HTTP connection pooling (`httpx.Client`) rather than creating new clients per request.
- **Verification**: Run `pytest test_reproduce.py -v`.
