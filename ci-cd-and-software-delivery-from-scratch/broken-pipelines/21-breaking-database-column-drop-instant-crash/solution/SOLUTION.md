# Solution: Broken Pipeline Lab 21 — Instant Column Drop Crashes Running Application Replicas

## 1. Root Cause Analysis
Destructive schema migration executed while old code replicas were still serving live traffic.

---

## 2. Step-by-Step Fix
Follow Expand / Migrate / Contract: deploy code that stops referencing the column first; drop column days later in a separate contract phase.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/21-breaking-database-column-drop-instant-crash/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Block destructive SQL operations (`DROP COLUMN`, `DROP TABLE`, `ALTER COLUMN TYPE`) in automated migration linters.
