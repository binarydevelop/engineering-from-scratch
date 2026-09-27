# Broken Backend Lab: Duplicate Financial Charges from Worker Retries

> **Category**: Queues  
> **Symptom**: Network timeout between worker and queue causes message re-delivery; customer is billed twice.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Network timeout between worker and queue causes message re-delivery; customer is billed twice.
```

## 2. Architecture & Context
This subsystem handles critical queues operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect payment transaction records; identify two charges with identical order ID.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Check unique idempotency key in database before executing payment side effects.
- **Verification**: Run `pytest test_reproduce.py -v`.
