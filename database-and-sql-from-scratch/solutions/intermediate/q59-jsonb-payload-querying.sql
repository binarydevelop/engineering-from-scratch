SELECT id, payload->>'env' AS env, payload->>'version' AS version FROM saas.events WHERE event_type = 'deploy.started' ORDER BY id ASC;
