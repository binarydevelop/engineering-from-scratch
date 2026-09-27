# Debugging Lab: Disk Full Log File Exhaustion

> **Category**: Operations

---

## 1. Symptom & Evidence
Application logs verbose debug statements to a single file without rotation until disk is full.

## 2. Root Cause Diagnosis
Operating system rejects all write operations with ENOSPC.

## 3. Architectural Fix
Implement size-based log rotation and retention policies.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-09-disk-full-log-file-exhaustion/test_reproduce.py -v
```
