# Broken Backend Lab: Silent Overwrite from Missing Version Check

> **Category**: Concurrency  
> **Symptom**: User A and User B edit document simultaneously; User B silently overwrites User A's changes.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
User A and User B edit document simultaneously; User B silently overwrites User A's changes.
```

## 2. Architecture & Context
This subsystem handles critical concurrency operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Audit update query; observe UPDATE lacks version condition.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Add `version` column and check `WHERE id = :id AND version = :expected_version`.
- **Verification**: Run `pytest test_reproduce.py -v`.
