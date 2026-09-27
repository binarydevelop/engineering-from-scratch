# Broken Backend Lab: Event Loop Freeze from Synchronous Sleep

> **Category**: Concurrency  
> **Symptom**: Single client calling slow endpoint freezes requests for all other concurrent users.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Single client calling slow endpoint freezes requests for all other concurrent users.
```

## 2. Architecture & Context
This subsystem handles critical concurrency operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Measure event loop lag; identify `time.sleep()` invoked inside `async def` handler.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Replace with `await asyncio.sleep()` or offload blocking function via `asyncio.to_thread`.
- **Verification**: Run `pytest test_reproduce.py -v`.
