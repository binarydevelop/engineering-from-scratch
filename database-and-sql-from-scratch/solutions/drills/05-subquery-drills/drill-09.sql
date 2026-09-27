SELECT user_id FROM social.likes
EXCEPT
SELECT user_id FROM social.posts
ORDER BY user_id ASC;
