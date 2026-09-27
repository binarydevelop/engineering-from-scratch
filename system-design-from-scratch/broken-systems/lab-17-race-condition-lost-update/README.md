# Debugging Lab: Race Condition Lost Update

> **Category**: Concurrency

---

## 1. Symptom & Evidence
Two concurrent requests read balance $100, calculate $100 - $30 = $70, and write back.

## 2. Root Cause Diagnosis
One debit overwrites the other, balance ends at $70 instead of $40.

## 3. Architectural Fix
Use atomic database update: UPDATE accounts SET balance = balance - 30 WHERE balance >= 30.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-17-race-condition-lost-update/test_reproduce.py -v
```
