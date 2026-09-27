SELECT
    f1.follower_id AS user_a_id,
    f1.following_id AS user_b_id
FROM social.follows f1
JOIN social.follows f2
    ON f1.follower_id = f2.following_id
    AND f1.following_id = f2.follower_id
WHERE f1.follower_id < f1.following_id
ORDER BY user_a_id ASC, user_b_id ASC;
