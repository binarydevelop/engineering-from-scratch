# Debugging Lab: Retry Storm Thundering Herd

> **Category**: Networking

---

## 1. Symptom & Evidence
5,000 clients retry failed service call immediately at the same instant.

## 2. Root Cause Diagnosis
Recovering service is instantly knocked down by synchronized retry burst.

## 3. Architectural Fix
Implement exponential backoff with full randomized jitter.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-20-retry-storm-thundering-herd/test_reproduce.py -v
```
