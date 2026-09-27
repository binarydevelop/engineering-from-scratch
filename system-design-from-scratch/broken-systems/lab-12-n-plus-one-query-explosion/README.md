# Debugging Lab: N+1 Query Explosion

> **Category**: Database

---

## 1. Symptom & Evidence
Endpoint fetches 100 users, then executes a separate query in a loop for each user's orders.

## 2. Root Cause Diagnosis
101 database queries executed for a single request, exhausting pool.

## 3. Architectural Fix
Eagerly join data or fetch related orders in a single batch query.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-12-n-plus-one-query-explosion/test_reproduce.py -v
```
