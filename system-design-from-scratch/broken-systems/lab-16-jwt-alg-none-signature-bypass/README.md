# Debugging Lab: JWT Alg=None Signature Bypass

> **Category**: Security

---

## 1. Symptom & Evidence
Token verification parser accepts alg: none in header without signature check.

## 2. Root Cause Diagnosis
Attacker crafts unsigned token forging admin privileges.

## 3. Architectural Fix
Explicitly whitelist expected cryptographic signing algorithms (e.g. HS256).

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-16-jwt-alg-none-signature-bypass/test_reproduce.py -v
```
