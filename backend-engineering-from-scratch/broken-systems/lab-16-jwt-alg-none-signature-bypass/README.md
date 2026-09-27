# Broken Backend Lab: JWT Signature Bypass via Alg: None Attack

> **Category**: Security  
> **Symptom**: Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.

---

## 1. The Symptom
In production, monitoring alerts fire:
```text
Attacker modifies JWT claims and changes header to 'alg: none'; server accepts forged token.
```

## 2. Architecture & Context
This subsystem handles critical security operations. Under standard single-request happy-path tests, the code appeared to function correctly. However, under production concurrency, failure conditions, or scale, the defect manifests.

## 3. Systematic Diagnostic Funnel
1. **Observe the Failure**: Reproduce the issue using `test_reproduce.py`.
2. **Inspect Telemetry**: Audit JWT verification options; observe algorithm whitelist was omitted.
3. **Isolate Root Cause**: Compare the implementation in `broken/` with expected protocol or database invariants.

## 4. The Fix
Review `fixed/` for the production-ready solution:
- **Remedy**: Explicitly enforce algorithms=['HS256'] in jwt.decode() to reject unsigned tokens.
- **Verification**: Run `pytest test_reproduce.py -v`.
