# Debugging Lab: Dual-Write Inconsistency

> **Category**: Consistency

---

## 1. Symptom & Evidence
Service writes order to database, then publishes event to Kafka; Kafka network call fails.

## 2. Root Cause Diagnosis
Database has order record, but downstream inventory/shipping workers never receive event.

## 3. Architectural Fix
Implement Transactional Outbox pattern committing event to local DB table.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-23-dual-write-inconsistency/test_reproduce.py -v
```
