# Solution: Broken Pipeline Lab 42 — Long-Running Migration Locks Table, Exhausting Connection Pool

## 1. Root Cause Analysis
Migration ran an unbatched update on 1,000,000 rows in a single transaction, holding an exclusive table lock.

---

## 2. Step-by-Step Fix
Chunk data migrations into small batches (e.g. 1,000 rows) with sleep pauses, or run backfills asynchronously.

---

## 3. Verification Command
To verify that the fix resolves the issue, run:
```bash
python3 broken-pipelines/42-database-migration-connection-pool-starvation/solution/verify_fix.py
```

---

## 4. Organizational Prevention Policy
> **Prevention Rule**: Mandate batching and timeout limits on all production database migrations.
