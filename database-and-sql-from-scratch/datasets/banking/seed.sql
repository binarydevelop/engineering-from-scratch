-- Financial & Banking Seed Data
SET search_path TO banking, public;

INSERT INTO customers (id, full_name, tax_id, risk_score, created_at) VALUES
(1, 'Morgan Vance', 'TAX-USA-1001', 15, '2025-01-10 09:00:00+00'),
(2, 'Jordan Hayes', 'TAX-USA-1002', 25, '2025-01-15 10:30:00+00'),
(3, 'Taylor Brooks', 'TAX-USA-1003', 80, '2025-02-01 14:00:00+00'),
(4, 'Casey Sterling', 'TAX-USA-1004', 10, '2025-03-01 11:15:00+00');

SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers));

INSERT INTO accounts (id, customer_id, account_number, account_type, balance, currency, version, is_frozen, created_at) VALUES
(1, 1, 'ACCT-CHK-10001', 'checking', 14500.50, 'USD', 12, FALSE, '2025-01-10 09:15:00+00'),
(2, 1, 'ACCT-SAV-10002', 'savings', 45000.00, 'USD', 5, FALSE, '2025-01-10 09:30:00+00'),
(3, 2, 'ACCT-CHK-20001', 'checking', 3200.75, 'USD', 8, FALSE, '2025-01-15 11:00:00+00'),
(4, 3, 'ACCT-CHK-30001', 'checking', 150.00, 'USD', 2, FALSE, '2025-02-01 14:15:00+00'),
(5, 4, 'ACCT-CHK-40001', 'checking', 250000.00, 'USD', 20, FALSE, '2025-03-01 11:30:00+00');

SELECT setval('accounts_id_seq', (SELECT MAX(id) FROM accounts));

-- Transactions and Double-Entry Ledger
INSERT INTO transactions (id, source_account_id, destination_account_id, amount, status, initiated_at, settled_at) VALUES
('a0000000-0000-0000-0000-000000000001', 1, 3, 500.00, 'posted', '2026-01-05 10:00:00+00', '2026-01-05 10:01:00+00'),
('a0000000-0000-0000-0000-000000000002', 3, 4, 150.00, 'posted', '2026-01-12 14:30:00+00', '2026-01-12 14:31:00+00'),
('a0000000-0000-0000-0000-000000000003', 5, 1, 10000.00, 'posted', '2026-02-01 09:00:00+00', '2026-02-01 09:02:00+00'),
('a0000000-0000-0000-0000-000000000004', 1, 2, 2000.00, 'posted', '2026-02-15 11:15:00+00', '2026-02-15 11:16:00+00'),
('a0000000-0000-0000-0000-000000000005', 4, 1, 500.00, 'failed', '2026-03-01 16:00:00+00', NULL); -- Failed due to insufficient funds

-- Ledger Entries (Double-Entry Bookkeeping: Every transfer has matching DEBIT and CREDIT)
INSERT INTO ledger_entries (id, transaction_id, account_id, entry_type, amount, running_balance, created_at) VALUES
(1, 'a0000000-0000-0000-0000-000000000001', 1, 'DEBIT', 500.00, 16000.50, '2026-01-05 10:01:00+00'),
(2, 'a0000000-0000-0000-0000-000000000001', 3, 'CREDIT', 500.00, 3350.75, '2026-01-05 10:01:00+00'),
(3, 'a0000000-0000-0000-0000-000000000002', 3, 'DEBIT', 150.00, 3200.75, '2026-01-12 14:31:00+00'),
(4, 'a0000000-0000-0000-0000-000000000002', 4, 'CREDIT', 150.00, 150.00, '2026-01-12 14:31:00+00'),
(5, 'a0000000-0000-0000-0000-000000000003', 5, 'DEBIT', 10000.00, 250000.00, '2026-02-01 09:02:00+00'),
(6, 'a0000000-0000-0000-0000-000000000003', 1, 'CREDIT', 10000.00, 16500.50, '2026-02-01 09:02:00+00'),
(7, 'a0000000-0000-0000-0000-000000000004', 1, 'DEBIT', 2000.00, 14500.50, '2026-02-15 11:16:00+00'),
(8, 'a0000000-0000-0000-0000-000000000004', 2, 'CREDIT', 2000.00, 45000.00, '2026-02-15 11:16:00+00');

SELECT setval('ledger_entries_id_seq', (SELECT MAX(id) FROM ledger_entries));
