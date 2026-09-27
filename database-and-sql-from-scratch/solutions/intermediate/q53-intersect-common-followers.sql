SELECT follower_id FROM social.follows WHERE following_id = 1 INTERSECT SELECT follower_id FROM social.follows WHERE following_id = 4 ORDER BY follower_id ASC;
