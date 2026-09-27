# Project: E-Commerce Batch Pipeline

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Project Overview
Extracts users, products, orders, payments from relational staging, transforms into dimensional facts/dimensions, and materializes sales mart.

## 2. Architectural Invariants
1. **Idempotency**: Rerunning the project logic on identical inputs produces identical target state.
2. **Contract Enforcement**: Input schemas and constraints are verified before state mutations.
3. **Traceability**: All output metrics and models trace cleanly to authoritative raw sources.

## 3. Directory Layout
- `code/main.py`: Core production implementation
- `tests/test_project.py`: Automated verification suite

## 4. Verification
Run the project test suite:
```bash
pytest projects/01-ecommerce-batch-pipeline/tests/test_project.py
```
