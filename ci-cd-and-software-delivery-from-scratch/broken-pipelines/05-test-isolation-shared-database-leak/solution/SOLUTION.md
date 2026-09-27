# Solution: Broken Pipeline Lab 05 — Parallel Test Shards Bleeding State into Shared Database

## 1. Root Cause Analysis
Parallel test runners shared the same SQLite/PostgreSQL database file and hardcoded fixture IDs without isolated schemas.

---

## 2. Step-by-Step Fix
Assign each parallel test worker a unique database URI or schema (e.g. `test_db_worker_${WORKER_ID}.sqlite3`) and wrap each test in a rolled-back transaction.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/05-test-isolation-shared-database-leak/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Enforce strict test database isolation per test worker.
