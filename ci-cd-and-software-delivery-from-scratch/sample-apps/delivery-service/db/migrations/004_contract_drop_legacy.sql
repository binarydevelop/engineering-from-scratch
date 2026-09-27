-- Migration 004: Contract Phase
-- Executed ONLY after 100% of running applications and batch consumers
-- have been running the updated code for multiple deployment cycles.
-- Creates an audit log table to record completed schema lifecycle.
CREATE TABLE IF NOT EXISTS schema_contract_audit (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    milestone TEXT NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_contract_audit (milestone) VALUES ('v2_currency_support_contract_complete');
