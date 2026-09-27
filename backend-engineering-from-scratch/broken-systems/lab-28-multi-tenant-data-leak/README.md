# Broken Backend Lab: Cross-Tenant Data Leak from Missing Scoping

> **Category**: Security  
> **Symptom**: User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
User in Tenant A accesses `/invoices/100` and views private invoice belonging to Tenant B.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect repository query; observe `SELECT * FROM invoices WHERE id = :id` lacks tenant filter.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Enforce tenant scoping on all queries: `WHERE id = :id AND tenant_id = :tenant_id`.
- **Verification**: Run `pytest test_reproduce.py -v`.
