# Broken Backend Lab: Deep Offset Pagination Query Timeout

> **Category**: Database  
> **Symptom**: Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Requesting `?page=5000&limit=20` takes 4.2 seconds; database scans 100,000 rows.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Run EXPLAIN ANALYZE on `OFFSET 100000`; observe full index scan and row discarding.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Refactor to Keyset/Cursor pagination: `WHERE id > :last_id ORDER BY id LIMIT 20`.
- **Verification**: Run `pytest test_reproduce.py -v`.
