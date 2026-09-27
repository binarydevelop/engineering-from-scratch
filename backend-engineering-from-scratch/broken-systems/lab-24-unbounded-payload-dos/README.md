# Broken Backend Lab: Denial of Service from Oversized JSON Body

> **Category**: Security  
> **Symptom**: Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Attacker sends 100MB JSON payload; server memory spikes and process is OOM-killed.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect request body reader; observe `await request.body()` reads arbitrary byte lengths.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Enforce maximum content-length validation and reject bodies exceeding 1MB with HTTP 413.
- **Verification**: Run `pytest test_reproduce.py -v`.
