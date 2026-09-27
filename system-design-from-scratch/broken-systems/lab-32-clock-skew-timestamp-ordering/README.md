# Debugging Lab: Clock Skew Timestamp Ordering

> **Category**: Distributed Systems

---

## 1. Symptom & Evidence
Two nodes use wall-clock datetime.now() for Last-Write-Wins conflict resolution.

## 2. Root Cause Diagnosis
Node with slow clock has newer update overwritten by older update from fast clock.

## 3. Architectural Fix
Use Lamport logical timestamps or version vectors instead of physical wall clocks.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-32-clock-skew-timestamp-ordering/test_reproduce.py -v
```
