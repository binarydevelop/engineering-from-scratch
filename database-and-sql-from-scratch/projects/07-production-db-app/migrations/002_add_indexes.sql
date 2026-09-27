-- Migration 002: Performance Indexes
CREATE INDEX IF NOT EXISTS idx_app_audit_entity ON app_audit_events(entity_type, entity_id);
CREATE INDEX IF NOT EXISTS idx_app_audit_created ON app_audit_events(created_at DESC);
