# Debugging Lab: CORS Wildcard Credential Leak

> **Category**: Security

---

## 1. Symptom & Evidence
API gateway configures Access-Control-Allow-Origin: * alongside credentials: true.

## 2. Root Cause Diagnosis
Malicious third-party websites can read authenticated user responses.

## 3. Architectural Fix
Enforce explicit domain allowlists for CORS origins.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-14-cors-wildcard-credential-leak/test_reproduce.py -v
```
