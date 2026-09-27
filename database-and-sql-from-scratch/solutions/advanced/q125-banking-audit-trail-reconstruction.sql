SELECT record_id, action, timestamp FROM banking.audit_log WHERE table_name = 'accounts' ORDER BY timestamp ASC;
