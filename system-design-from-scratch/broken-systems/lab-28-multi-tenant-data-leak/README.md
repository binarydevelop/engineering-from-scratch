# Debugging Lab: Multi-Tenant Data Leak

> **Category**: Security

---

## 1. Symptom & Evidence
SQL query retrieves documents using WHERE id = ? omitting tenant_id filter.

## 2. Root Cause Diagnosis
Tenant A views Tenant B's confidential documents by guessing ID.

## 3. Architectural Fix
Enforce mandatory tenant_id scoping in repository query layer.

---

## 4. Verification
Execute the automated test suite reproducing the failure and confirming the resolution:
```bash
pytest broken-systems/lab-28-multi-tenant-data-leak/test_reproduce.py -v
```
