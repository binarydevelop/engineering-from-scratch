# Broken Backend Lab: N+1 Query Explosion on Relationship Endpoint

> **Category**: Database  
> **Symptom**: Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Fetching 50 users triggers 51 separate SQL queries, degrading endpoint latency to 300ms.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Enable SQL statement echo logging; count executed SELECT queries per request.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Use eager loading (`selectinload` or SQL JOIN) to reduce 51 queries to 2 queries.
- **Verification**: Run `pytest test_reproduce.py -v`.
