# Broken Backend Lab: Lost Update Anomaly Under Concurrent Purchases

> **Category**: Concurrency  
> **Symptom**: Two simultaneous purchases of the last item both succeed; stock is oversold to -1.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Two simultaneous purchases of the last item both succeed; stock is oversold to -1.
```

## 2. Architecture & Context
This subsystem handles critical concurrency operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect concurrent transaction traces; observe read-modify-write without row locks.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Apply pessimistic row locking (`SELECT FOR UPDATE`) or atomic SQL decrement expressions.
- **Verification**: Run `pytest test_reproduce.py -v`.
