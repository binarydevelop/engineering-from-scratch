# Solution: Broken Pipeline Lab 29 — Monorepo Pipeline Skips Testing Downstream Dependent Service

## 1. Root Cause Analysis
Change detection script only checked git diff against the service's own directory (`services/service-b/`), ignoring shared lib dependencies.

---

## 2. Step-by-Step Fix
Model the internal monorepo dependency graph: changes to shared libraries trigger tests for all downstream dependents.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/29-monorepo-change-detector-misses-shared-lib-change/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Use graph-aware build tools (Bazel, Nx, Turborepo, or custom DAG matrix).
