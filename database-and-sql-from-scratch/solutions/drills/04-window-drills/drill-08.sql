SELECT
    id,
    entry_type,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY account_id ORDER BY created_at ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS first_entry_amount,
    LAST_VALUE(amount) OVER (
        PARTITION BY account_id ORDER BY created_at ASC
        ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_entry_amount
FROM banking.ledger_entries
WHERE account_id = 1
ORDER BY created_at ASC;
