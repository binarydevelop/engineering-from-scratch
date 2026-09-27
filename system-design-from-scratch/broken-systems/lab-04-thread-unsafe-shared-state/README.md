# Debugging Lab: Thread-Unsafe Shared Memory State

> **Category**: Concurrency

---

## 1. Symptom & Evidence
Concurrent worker threads increment shared dictionary counter without synchronization.

## 2. Root Cause Diagnosis
Race condition corrupts counter state under high thread concurrency.

## 3. Architectural Fix
Protect counter mutation with threading.Lock or atomic primitives.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-04-thread-unsafe-shared-state/test_reproduce.py -v
```
