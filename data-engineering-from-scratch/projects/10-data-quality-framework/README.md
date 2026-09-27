# Project: Declarative Data Quality Engine

> **Motto**: Understand it. Ingest it. Model it. Transform it. Validate it. Break it. Recover it. Scale it. Operate it.

---

## 1. Project Overview
Implements assertions (NotNull, Unique, AcceptedValues, RangeBound) and produces structured quality run reports.

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
pytest projects/10-data-quality-framework/tests/test_project.py
```
