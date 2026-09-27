SELECT s.id AS missing_id FROM generate_series(1, 10) AS s(id) LEFT JOIN banking.accounts a ON s.id = a.id WHERE a.id IS NULL ORDER BY missing_id ASC;
