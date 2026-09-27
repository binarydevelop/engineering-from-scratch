CREATE TABLE lab.accounts (
    id SERIAL PRIMARY KEY,
    balance NUMERIC(12, 2) NOT NULL CHECK (balance >= 0.00)
);
