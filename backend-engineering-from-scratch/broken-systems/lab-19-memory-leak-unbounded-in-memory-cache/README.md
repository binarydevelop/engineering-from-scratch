# Broken Backend Lab: Process OOM from Unbounded Global Cache

> **Category**: Performance  
> **Symptom**: Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Application memory RSS grows linearly with requests until process is terminated by OS OOM killer.
```

## 2. Architecture & Context
This subsystem handles critical performance operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Compare memory snapshots with `tracemalloc`; identify global dictionary retaining request objects.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Replace unbounded dictionary with a bounded LRU cache (`cachetools.LRUCache(maxsize=1000)`).
- **Verification**: Run `pytest test_reproduce.py -v`.
