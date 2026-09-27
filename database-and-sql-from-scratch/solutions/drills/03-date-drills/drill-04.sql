SELECT
    p.id AS post_id,
    ROUND(EXTRACT(EPOCH FROM (MIN(c.created_at) - p.created_at)) / 3600.0, 2) AS duration_hours
FROM social.posts p
JOIN social.comments c ON p.id = c.post_id
WHERE p.id = 1
GROUP BY p.id, p.created_at;
