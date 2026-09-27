SELECT id, balance, version, (balance >= 500.00 AND version = 12) AS is_updatable FROM banking.accounts WHERE id = 1;
