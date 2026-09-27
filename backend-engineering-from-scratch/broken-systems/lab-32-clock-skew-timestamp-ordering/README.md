# Broken Backend Lab: Event Ordering Failure Due to Server Clock Skew

> **Category**: Distributed  
> **Symptom**: Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Event A occurred before Event B, but Event B has an earlier timestamp due to unsynchronized clocks.
```

## 2. Architecture & Context
This subsystem handles critical distributed operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Compare event timestamps across multi-node cluster; observe 500ms server clock drift.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Use logical sequence numbers or monotonically increasing database IDs instead of wall clocks.
- **Verification**: Run `pytest test_reproduce.py -v`.
