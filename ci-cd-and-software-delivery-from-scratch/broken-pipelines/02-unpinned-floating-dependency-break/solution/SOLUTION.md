# Solution: Broken Pipeline Lab 02 — Floating Dependency Range Pulls Breaking Upstream Release

## 1. Root Cause Analysis
Dependency specification in package manager used floating range (`requests>=2.0.0` or `fastapi^0.100.0`), pulling a newly published breaking release.

---

## 2. Step-by-Step Fix
Generate and enforce an exact lockfile (`pip-compile`, `poetry.lock`, or `package-lock.json`) with pinned hashes.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/02-unpinned-floating-dependency-break/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Enforce `--frozen-lockfile` or `--require-hashes` in CI dependency installation steps.
