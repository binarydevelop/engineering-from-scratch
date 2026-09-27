SELECT COUNT(*) AS dark_mode_updates FROM saas.events WHERE event_type = 'settings.updated' AND (payload->'feature_flags'->>'dark_mode')::BOOLEAN = TRUE;
