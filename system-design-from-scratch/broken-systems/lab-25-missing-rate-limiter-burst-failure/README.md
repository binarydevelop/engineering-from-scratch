# Debugging Lab: Missing Rate Limiter Burst Failure

> **Category**: Traffic

---

## 1. Symptom & Evidence
API accepts unlimited requests per second from single rogue API key.

## 2. Root Cause Diagnosis
Legitimate users starved of compute resources during attack.

## 3. Architectural Fix
Place Token Bucket rate limiter at the API gateway.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-25-missing-rate-limiter-burst-failure/test_reproduce.py -v
```
