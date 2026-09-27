SELECT id, device_type, ROUND(EXTRACT(EPOCH FROM (ended_at - started_at)) / 60.0, 2) AS duration_minutes FROM analytics.sessions WHERE ended_at IS NOT NULL ORDER BY duration_minutes DESC;
