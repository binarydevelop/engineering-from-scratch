# Solution: Broken Pipeline Lab 20 — Missing Environment Variable Causes Instant Crash on First Request

## 1. Root Cause Analysis
Application lacked a startup validation check for required environment variable `JWT_SECRET`; it crashed only when the first request arrived.

---

## 2. Step-by-Step Fix
Validate all critical configuration on process startup and fail fast during initialization so readiness probe fails before traffic route.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/20-deploy-succeeds-but-app-crashes-on-startup/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Include post-deployment smoke tests that invoke real authenticated API paths.
