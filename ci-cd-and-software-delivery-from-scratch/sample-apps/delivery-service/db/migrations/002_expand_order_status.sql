-- Migration 002: Expand Phase (Backward-Compatible Schema Change)
-- Adding new column 'currency' with a safe default value.
-- Old application replicas can continue running and inserting without knowing about 'currency'.
ALTER TABLE orders ADD COLUMN currency TEXT NOT NULL DEFAULT 'USD';
