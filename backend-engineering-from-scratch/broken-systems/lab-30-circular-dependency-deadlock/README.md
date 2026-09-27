# Broken Backend Lab: Distributed Deadlock Between Two Microservices

> **Category**: Architecture  
> **Symptom**: Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Service A calls Service B, which synchronously calls Service A back; both thread pools exhaust.
```

## 2. Architecture & Context
This subsystem handles critical architecture operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect distributed trace; identify circular synchronous HTTP dependency chain.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Break circular call: pass required data forward in initial payload or use asynchronous events.
- **Verification**: Run `pytest test_reproduce.py -v`.
