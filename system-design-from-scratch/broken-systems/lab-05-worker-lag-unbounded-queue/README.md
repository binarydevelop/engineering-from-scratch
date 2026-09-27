# Debugging Lab: Worker Lag on Unbounded Queue

> **Category**: Queues

---

## 1. Symptom & Evidence
Producers write at 10,000 msg/s while consumers process 1,000 msg/s with no queue bounds.

## 2. Root Cause Diagnosis
Unbounded queue consumes all available heap memory, causing OOM crash.

## 3. Architectural Fix
Implement bounded queue with backpressure rejection (HTTP 429).

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-05-worker-lag-unbounded-queue/test_reproduce.py -v
```
