SELECT id, created_at, entry_type, amount, running_balance FROM banking.ledger_entries WHERE account_id = 1 ORDER BY created_at ASC;
