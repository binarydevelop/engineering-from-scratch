# Debugging Lab: Unhandled SIGTERM Dirty Shutdown

> **Category**: Operations

---

## 1. Symptom & Evidence
Kubernetes sends SIGTERM; application terminates instantly killing in-flight requests.

## 2. Root Cause Diagnosis
Clients experience connection reset and partial database writes.

## 3. Architectural Fix
Trap SIGTERM, cease accepting new requests, and allow in-flight requests 15s to drain.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-29-unhandled-sigterm-dirty-shutdown/test_reproduce.py -v
```
