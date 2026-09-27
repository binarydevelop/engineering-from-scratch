# Broken Backend Lab: Credential Stuffing on Unthrottled Login

> **Category**: Security  
> **Symptom**: Attacker submits 5,000 password guesses per minute against `/login` without restriction.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Attacker submits 5,000 password guesses per minute against `/login` without restriction.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Inspect auth access logs; observe high volume of failed logins from single IP.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Install Token Bucket rate limiter capping authentication attempts to 5 per minute per IP.
- **Verification**: Run `pytest test_reproduce.py -v`.
