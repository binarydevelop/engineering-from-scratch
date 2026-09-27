# Solution: Broken Pipeline Lab 07 — Cache Key Ignores Lockfile Hash, Serving Stale Packages

## 1. Root Cause Analysis
Cache key was hardcoded as `key: python-deps-${{ runner.os }}` without hashing `requirements.lock`.

---

## 2. Step-by-Step Fix
Include lockfile hash in cache key: `key: python-deps-${{ runner.os }}-${{ hashFiles('requirements.lock') }}`.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/07-stale-cache-bad-key/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Audit cache key definitions to ensure every key incorporates a cryptographic hash of its inputs.
