SELECT
    event_name,
    event_timestamp,
    EXTRACT(EPOCH FROM (event_timestamp - LAG(event_timestamp) OVER (ORDER BY event_timestamp))) AS seconds_since_prev
FROM analytics.events
WHERE session_id = 'b0000000-0000-0000-0000-000000000001'
ORDER BY event_timestamp ASC;
