# Solution: Broken Pipeline Lab 06 — Poisoned Dependency Cache Restoring Corrupted Binaries

## 1. Root Cause Analysis
A previous canceled job was terminated mid-write while writing into the cache directory, storing half-written truncated files under the cache key.

---

## 2. Step-by-Step Fix
Write caches to a temporary directory first and atomically rename upon step completion; bust cache by updating cache key version prefix.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/06-poisoned-dependency-cache/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Only cache on successful step exit (`if: success()`), never on canceled jobs.
