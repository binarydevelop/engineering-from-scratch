# Broken Backend Lab: Service Outage Caused by Unrotated Log Files

> **Category**: Operational  
> **Symptom**: Database writes fail with `IOError: [Errno 28] No space left on device`.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Database writes fail with `IOError: [Errno 28] No space left on device`.
```

## 2. Architecture & Context
This subsystem handles critical operational operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Run `df -h` and `du -sh *` to locate multi-gigabyte unrotated application log file.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Truncate log file, restore service, and configure logrotate with max size limits.
- **Verification**: Run `pytest test_reproduce.py -v`.
