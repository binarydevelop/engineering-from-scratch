# Debugging Lab: Circuit Breaker Stuck Open

> **Category**: Resilience

---

## 1. Symptom & Evidence
Circuit breaker opens on failure but never checks if downstream has recovered.

## 2. Root Cause Diagnosis
Service permanently fast-fails requests even after downstream heals.

## 3. Architectural Fix
Add HALF_OPEN state probe after recovery cooldown timeout.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-21-circuit-breaker-stuck-open/test_reproduce.py -v
```
