# Broken Backend Lab: Slow API Due to Missing Database Index

> **Category**: Database  
> **Symptom**: p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
p99 latency increases from 5ms to 2500ms as table row count grows; CPU is idle waiting for disk I/O.
```

## 2. Architecture & Context
This subsystem handles critical database operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect EXPLAIN ANALYZE execution plan to identify Seq Scan on filter predicate.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Add B-Tree index on filtered foreign key column.
- **Verification**: Run `pytest test_reproduce.py -v`.
