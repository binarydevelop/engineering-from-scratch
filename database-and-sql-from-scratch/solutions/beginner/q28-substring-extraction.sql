SELECT id, account_number, SUBSTRING(account_number FROM 6 FOR 3) AS acct_code FROM banking.accounts ORDER BY id ASC;
