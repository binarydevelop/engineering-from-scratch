SELECT u.id, u.username FROM social.users u WHERE EXISTS (SELECT 1 FROM social.posts p JOIN social.comments c ON p.id = c.post_id WHERE p.user_id = u.id) ORDER BY u.id ASC;
