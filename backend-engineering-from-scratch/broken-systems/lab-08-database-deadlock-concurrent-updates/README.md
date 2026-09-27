# Broken Backend Lab: Database Deadlock on Inverted Lock Acquisition

> **Category**: Database  
> **Symptom**: Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Concurrent transfers between Account A and Account B trigger SQL 40P01 Deadlock Detected.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect PostgreSQL lock logs; observe Tx 1 locks A then B while Tx 2 locks B then A.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Enforce consistent global locking order: always lock smaller account ID first.
- **Verification**: Run `pytest test_reproduce.py -v`.
