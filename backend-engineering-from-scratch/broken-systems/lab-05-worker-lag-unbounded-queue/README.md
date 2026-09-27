# Broken Backend Lab: Worker Queue Lag and Unbounded Growth

> **Category**: Queues  
> **Symptom**: Queue depth grows continuously; worker memory usage swells until process is OOM-killed.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Queue depth grows continuously; worker memory usage swells until process is OOM-killed.
```

## 2. Architecture & Context
This subsystem handles critical queues operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Measure queue arrival rate vs processing rate; identify unbounded memory queue buffer.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Enforce bounded queue with maxsize and apply upstream backpressure or load shedding.
- **Verification**: Run `pytest test_reproduce.py -v`.
