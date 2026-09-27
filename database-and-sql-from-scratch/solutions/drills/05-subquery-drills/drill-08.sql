SELECT user_id FROM social.posts
UNION
SELECT user_id FROM social.comments
ORDER BY user_id ASC;
