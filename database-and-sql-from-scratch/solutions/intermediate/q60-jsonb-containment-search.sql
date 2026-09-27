SELECT id, event_type, created_at FROM saas.events WHERE payload @> '{"gpu": "h100"}'::jsonb ORDER BY id ASC;
