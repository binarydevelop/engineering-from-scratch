# Project: Full GitHub Actions CI Pipeline (Phase 207)

## 1. Project Goal
Build an end-to-end pull request validation pipeline enforcing static analysis, parallelized unit testing, integration testing, and bytecode verification.

---

## 2. Core Architectural Deliverables
- [ ] YAML workflow `.github/workflows/ci.yml`
- [ ] Top-level empty permissions with explicit least-privilege job grants
- [ ] Concurrency group cancelling superseded runs
- [ ] Diagnostic test artifact upload with retention limits

---

## 3. Verification Command
To verify your project implementation, execute:
```bash
python3 projects/02-full-actions-ci/verify.py
```
