# Debugging Lab: Circular Dependency Deadlock

> **Category**: Microservices

---

## 1. Symptom & Evidence
Service A calls Service B, which synchronously calls Service A to verify permissions.

## 2. Root Cause Diagnosis
Both services exhaust thread pools waiting on each other.

## 3. Architectural Fix
Decouple circular calls using token propagation or asynchronous events.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-30-circular-dependency-deadlock/test_reproduce.py -v
```
