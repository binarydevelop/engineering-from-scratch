# Debugging Lab: Transaction Boundary Too Broad

> **Category**: Database

---

## 1. Symptom & Evidence
Database transaction remains open while application makes 5-second 3rd party HTTP call.

## 2. Root Cause Diagnosis
Database row locks held for 5 seconds, causing connection starvation.

## 3. Architectural Fix
Commit database transaction before initiating external network calls.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-22-transaction-boundary-too-broad/test_reproduce.py -v
```
