# Solution: Broken Pipeline Lab 04 — Flaky Asynchronous Race Condition in Integration Suite

## 1. Root Cause Analysis
Test used arbitrary `time.sleep(0.1)` instead of polling with timeout on asynchronous queue completion.

---

## 2. Step-by-Step Fix
Replace hardcoded sleep timers with deterministic condition polling (`wait_until(lambda: get_status() == 'completed', timeout=5)`).

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/04-flaky-test-race-condition/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Quarantine flaky tests immediately. Never allow test retries to normalize non-deterministic test suites.
