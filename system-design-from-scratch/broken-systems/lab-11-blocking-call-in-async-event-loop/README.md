# Debugging Lab: Blocking Call in Async Event Loop

> **Category**: Async/IO

---

## 1. Symptom & Evidence
Asynchronous route handler invokes synchronous time.sleep or disk I/O.

## 2. Root Cause Diagnosis
Event loop freezes; all concurrent async requests stall.

## 3. Architectural Fix
Replace synchronous calls with asyncio.sleep or run in executor thread.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-11-blocking-call-in-async-event-loop/test_reproduce.py -v
```
