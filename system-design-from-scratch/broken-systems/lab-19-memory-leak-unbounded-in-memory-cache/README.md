# Debugging Lab: Memory Leak Unbounded In-Memory Cache

> **Category**: Caching

---

## 1. Symptom & Evidence
In-memory Python dictionary caches query results without TTL or size limits.

## 2. Root Cause Diagnosis
Process RSS memory grows continuously until OS kills process (OOM).

## 3. Architectural Fix
Implement bounded LRU cache with eviction.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-19-memory-leak-unbounded-in-memory-cache/test_reproduce.py -v
```
