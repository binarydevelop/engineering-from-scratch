# Debugging Lab: Ephemeral Port Exhaustion

> **Category**: Networking

---

## 1. Symptom & Evidence
HTTP client creates fresh TCP connection for every outbound request without pooling.

## 2. Root Cause Diagnosis
TIME_WAIT sockets exhaust OS ephemeral port range (65,535).

## 3. Architectural Fix
Reuse persistent connections using an HTTP connection pool.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-26-ephemeral-port-exhaustion/test_reproduce.py -v
```
