-- Financial & Banking Relational Schema
CREATE SCHEMA IF NOT EXISTS banking;
SET search_path TO banking, public;

DROP TABLE IF EXISTS audit_log CASCADE;
DROP TABLE IF EXISTS ledger_entries CASCADE;
DROP TABLE IF EXISTS transactions CASCADE;
DROP TABLE IF EXISTS accounts CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    tax_id VARCHAR(50) NOT NULL UNIQUE,
    risk_score INT NOT NULL DEFAULT 50 CHECK (risk_score BETWEEN 0 AND 100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE accounts (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(id),
    account_number VARCHAR(34) NOT NULL UNIQUE,
    account_type VARCHAR(20) NOT NULL CHECK (account_type IN ('checking', 'savings', 'escrow')),
    balance NUMERIC(14, 2) NOT NULL DEFAULT 0.00 CHECK (balance >= 0.00), -- Invariant: Non-negative balance
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    version INT NOT NULL DEFAULT 1, -- Optimistic concurrency control version
    is_frozen BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_account_id INT NOT NULL REFERENCES accounts(id),
    destination_account_id INT NOT NULL REFERENCES accounts(id),
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'posted', 'failed', 'reversed')),
    initiated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    settled_at TIMESTAMPTZ,
    CHECK (source_account_id != destination_account_id)
);

CREATE TABLE ledger_entries (
    id BIGSERIAL PRIMARY KEY,
    transaction_id UUID NOT NULL REFERENCES transactions(id),
    account_id INT NOT NULL REFERENCES accounts(id),
    entry_type VARCHAR(6) NOT NULL CHECK (entry_type IN ('DEBIT', 'CREDIT')),
    amount NUMERIC(14, 2) NOT NULL CHECK (amount > 0),
    running_balance NUMERIC(14, 2) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    action VARCHAR(10) NOT NULL,
    record_id VARCHAR(64) NOT NULL,
    old_state JSONB,
    new_state JSONB,
    performed_by VARCHAR(50) NOT NULL DEFAULT CURRENT_USER,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_accounts_customer ON accounts(customer_id);
CREATE INDEX idx_ledger_account_created ON ledger_entries(account_id, created_at);
CREATE INDEX idx_transactions_source ON transactions(source_account_id, initiated_at);
