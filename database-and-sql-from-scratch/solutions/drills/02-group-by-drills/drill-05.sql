SELECT
    p.user_id AS author_id,
    COUNT(DISTINCT l.user_id) AS unique_likers_count
FROM social.posts p
JOIN social.likes l ON p.id = l.post_id
WHERE p.user_id = 1
GROUP BY p.user_id;
