SELECT
    event_name,
    event_timestamp,
    LEAD(event_name, 1) OVER (ORDER BY event_timestamp ASC) AS next_event_name
FROM analytics.events
WHERE session_id = 'b0000000-0000-0000-0000-000000000001'
ORDER BY event_timestamp ASC;
