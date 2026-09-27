# Debugging Lab: Optimistic Locking Collision Storm

> **Category**: Concurrency

---

## 1. Symptom & Evidence
High-concurrency updates on hot row cause version conflicts, triggering infinite unjittered retries.

## 2. Root Cause Diagnosis
Database CPU spikes to 100% rejecting retry attempts.

## 3. Architectural Fix
Combine optimistic locking with exponential backoff and retry budgets.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-18-optimistic-locking-collision/test_reproduce.py -v
```
