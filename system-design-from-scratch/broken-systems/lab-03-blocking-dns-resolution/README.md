# Debugging Lab: Blocking DNS Resolution

> **Category**: Networking

---

## 1. Symptom & Evidence
Synchronous socket DNS resolution blocks the asynchronous worker loop.

## 2. Root Cause Diagnosis
gethostbyname blocks the entire event loop thread.

## 3. Architectural Fix
Use non-blocking asynchronous resolver or local DNS caching.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-03-blocking-dns-resolution/test_reproduce.py -v
```
