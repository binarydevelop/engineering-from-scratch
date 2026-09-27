# Debugging Lab: Unbounded Payload Denial of Service

> **Category**: Security

---

## 1. Symptom & Evidence
API reads request body with f.read() into memory without Content-Length limit.

## 2. Root Cause Diagnosis
Attacker sends 10 GB payload causing instant memory exhaustion.

## 3. Architectural Fix
Enforce strict maximum body size limits at reverse proxy/middleware.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-24-unbounded-payload-dos/test_reproduce.py -v
```
