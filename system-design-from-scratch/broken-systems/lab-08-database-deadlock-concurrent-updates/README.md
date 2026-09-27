# Debugging Lab: Database Deadlock on Concurrent Updates

> **Category**: Database

---

## 1. Symptom & Evidence
Transaction 1 locks Row A then Row B; Transaction 2 locks Row B then Row A.

## 2. Root Cause Diagnosis
Circular lock wait results in database deadlock exception.

## 3. Architectural Fix
Enforce canonical lock ordering (always lock in ascending ID order).

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-08-database-deadlock-concurrent-updates/test_reproduce.py -v
```
