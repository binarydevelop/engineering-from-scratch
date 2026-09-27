SELECT following_id FROM social.follows WHERE follower_id = 1 EXCEPT SELECT follower_id FROM social.follows WHERE following_id = 1 ORDER BY following_id ASC;
