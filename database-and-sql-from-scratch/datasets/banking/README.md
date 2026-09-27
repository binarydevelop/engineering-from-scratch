# Financial & Banking Dataset

A mission-critical financial ledger modeling customers, checking/savings accounts, double-entry bookkeeping, optimistic locking, and strict audit logs.

## Entity-Relationship Diagram

```text
  [customers] 1 ──── N [accounts]
                          │
          ┌───────────────┴───────────────┐
          │ source_account_id             │ destination_account_id
          ▼                               ▼
     [transactions] 1 ────────── N [ledger_entries] (DEBIT & CREDIT)
```

## Key Relational Invariants
- **Non-Negative Balance:** Enforced via `CHECK (balance >= 0.00)`.
- **Double-Entry Balance Constraint:** Every settled transaction generates exactly two ledger entries (1 DEBIT, 1 CREDIT) summing to 0 delta.
- **Optimistic Concurrency Control:** Accounts feature an incrementing `version` column for high-throughput non-blocking updates.
- **Audit Immutability:** The `audit_log` records state diffs using `JSONB`.
