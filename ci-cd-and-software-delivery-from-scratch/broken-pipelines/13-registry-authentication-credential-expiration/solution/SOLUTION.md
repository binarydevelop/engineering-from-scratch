# Solution: Broken Pipeline Lab 13 — Docker Push Fails at End of 45-Minute Build Job

## 1. Root Cause Analysis
Registry login token had a 30-minute expiration window and expired while tests were running.

---

## 2. Step-by-Step Fix
Separate build/test job from publish job; authenticate registry immediately prior to push in a dedicated short job.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/13-registry-authentication-credential-expiration/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Keep registry publishing jobs short and decoupled from lengthy test suites.
