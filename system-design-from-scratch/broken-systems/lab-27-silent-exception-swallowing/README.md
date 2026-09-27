# Debugging Lab: Silent Exception Swallowing

> **Category**: Reliability

---

## 1. Symptom & Evidence
Worker wraps critical persistence code in except Exception: pass.

## 2. Root Cause Diagnosis
Failures fail silently; data is permanently lost without alerts.

## 3. Architectural Fix
Log exception with traceback and raise or re-queue message.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-27-silent-exception-swallowing/test_reproduce.py -v
```
