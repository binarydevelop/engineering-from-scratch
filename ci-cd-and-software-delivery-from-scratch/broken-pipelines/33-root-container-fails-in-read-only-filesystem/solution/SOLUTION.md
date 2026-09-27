# Solution: Broken Pipeline Lab 33 — Container Assumes Root Access and Writable Root Filesystem

## 1. Root Cause Analysis
Kubernetes security policy enforced `readOnlyRootFilesystem: true` and `runAsNonRoot: true`.

---

## 2. Step-by-Step Fix
Run as non-root user and mount `emptyDir` volumes to specific writable directories (`/tmp`, `/app/cache`).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/33-root-container-fails-in-read-only-filesystem/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Test container images locally under non-root and read-only flags (`docker run --read-only`).
