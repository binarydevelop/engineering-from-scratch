# Debugging Lab: Offset Pagination Deep Scan Latency

> **Category**: Database

---

## 1. Symptom & Evidence
Client requests SELECT * FROM logs ORDER BY id LIMIT 20 OFFSET 1000000.

## 2. Root Cause Diagnosis
Database reads and discards 1,000,000 rows, taking 8 seconds per page.

## 3. Architectural Fix
Replace OFFSET with Keyset/Cursor pagination (WHERE id > ? ORDER BY id LIMIT 20).

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-31-offset-pagination-deep-scan-latency/test_reproduce.py -v
```
