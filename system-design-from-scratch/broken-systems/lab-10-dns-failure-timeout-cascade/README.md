# Debugging Lab: DNS Failure Timeout Cascade

> **Category**: Networking

---

## 1. Symptom & Evidence
DNS provider encounters transient failure; backend attempts fresh lookup per request with no cache.

## 2. Root Cause Diagnosis
All downstream HTTP requests hang until 30s socket timeout.

## 3. Architectural Fix
Configure local DNS resolution caching with explicit TTL.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-10-dns-failure-timeout-cascade/test_reproduce.py -v
```
