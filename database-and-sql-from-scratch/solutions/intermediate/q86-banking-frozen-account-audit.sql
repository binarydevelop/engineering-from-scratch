SELECT a.account_number, c.full_name, a.balance FROM banking.accounts a JOIN banking.customers c ON a.customer_id = c.id WHERE a.is_frozen = TRUE ORDER BY a.balance DESC;
