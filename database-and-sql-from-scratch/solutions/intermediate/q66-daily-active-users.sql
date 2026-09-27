SELECT event_timestamp::DATE AS event_day, COUNT(DISTINCT user_id) AS dau FROM analytics.events GROUP BY 1 ORDER BY event_day ASC;
