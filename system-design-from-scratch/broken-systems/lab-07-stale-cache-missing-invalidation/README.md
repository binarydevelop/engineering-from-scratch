# Debugging Lab: Stale Cache Missing Invalidation

> **Category**: Caching

---

## 1. Symptom & Evidence
Database record is updated directly, but corresponding cache key is never invalidated.

## 2. Root Cause Diagnosis
Readers query cache and receive stale data indefinitely.

## 3. Architectural Fix
Implement transactional cache invalidation on write path.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-07-stale-cache-missing-invalidation/test_reproduce.py -v
```
