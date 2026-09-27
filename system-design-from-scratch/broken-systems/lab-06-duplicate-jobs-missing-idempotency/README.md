# Debugging Lab: Duplicate Jobs Due to Missing Idempotency

> **Category**: Queues

---

## 1. Symptom & Evidence
Worker crashes after charging customer but before acknowledging queue message, causing duplicate charges on retry.

## 2. Root Cause Diagnosis
At-least-once message redelivery executes non-idempotent credit card charge twice.

## 3. Architectural Fix
Enforce unique idempotency key check before charging payment.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-06-duplicate-jobs-missing-idempotency/test_reproduce.py -v
```
