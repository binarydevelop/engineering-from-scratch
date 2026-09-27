# Debugging Lab: Connection Leak Pool Exhaustion

> **Category**: Resources

---

## 1. Symptom & Evidence
Database connection pool exhausts after errors because connections are not released in finally blocks.

## 2. Root Cause Diagnosis
Exception occurs during query, connection remains checked out indefinitely.

## 3. Architectural Fix
Wrap connection checkout in RAII context manager or try/finally block.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-01-connection-leak-pool-exhaustion/test_reproduce.py -v
```
