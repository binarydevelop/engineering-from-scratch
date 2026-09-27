# Solution: Broken Pipeline Lab 03 — Developer Machine Uses Different Transitive Dependency than CI

## 1. Root Cause Analysis
The lockfile was omitted from git commit (`.gitignore` had `*.lock` mistakenly), causing CI to resolve latest transitive sub-dependencies.

---

## 2. Step-by-Step Fix
Commit canonical lockfiles to git and verify lockfile presence in pre-commit hooks.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/03-missing-lockfile-drift/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Add CI preflight check ensuring lockfile exists and matches direct manifest requirements.
