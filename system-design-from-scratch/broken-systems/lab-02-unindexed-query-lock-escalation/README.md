# Debugging Lab: Unindexed Query Lock Escalation

> **Category**: Database

---

## 1. Symptom & Evidence
Concurrent queries on unindexed column trigger sequential table scans, escalating row locks to table locks.

## 2. Root Cause Diagnosis
Query without index scans entire table holding shared locks.

## 3. Architectural Fix
Add B-Tree index on queried column to enable index seek.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-02-unindexed-query-lock-escalation/test_reproduce.py -v
```
