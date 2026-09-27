# Debugging Lab: CSRF Vulnerable Cookie Session

> **Category**: Security

---

## 1. Symptom & Evidence
State-changing POST requests rely on session cookies without anti-CSRF protection.

## 2. Root Cause Diagnosis
Cross-site request triggers unauthorized user action.

## 3. Architectural Fix
Enforce SameSite=Strict cookies and anti-CSRF token verification.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-15-csrf-vulnerable-cookie-session/test_reproduce.py -v
```
