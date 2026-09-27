SELECT id, account_number, balance, (balance + 500.00) AS new_balance FROM banking.accounts WHERE account_type = 'checking' ORDER BY id ASC;
