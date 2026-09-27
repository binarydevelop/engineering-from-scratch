-- Social Network Queries
SET search_path TO social, public;

-- 1. Follower and Following Counts per User
SELECT 
    u.id,
    u.username,
    COUNT(DISTINCT f_in.follower_id) AS followers_count,
    COUNT(DISTINCT f_out.following_id) AS following_count
FROM users u
LEFT JOIN follows f_in ON u.id = f_in.following_id
LEFT JOIN follows f_out ON u.id = f_out.follower_id
GROUP BY u.id, u.username
ORDER BY followers_count DESC, u.id ASC;

-- 2. Mutual Follows (Bidirectional Friendships)
SELECT 
    f1.follower_id AS user_a,
    u1.username AS user_a_name,
    f1.following_id AS user_b,
    u2.username AS user_b_name
FROM follows f1
JOIN follows f2 ON f1.follower_id = f2.following_id AND f1.following_id = f2.follower_id
JOIN users u1 ON f1.follower_id = u1.id
JOIN users u2 ON f1.following_id = u2.id
WHERE f1.follower_id < f1.following_id
ORDER BY user_a ASC, user_b ASC;

-- 3. Popular Posts by Likes and Comments
SELECT 
    p.id AS post_id,
    u.username AS author,
    p.content,
    COUNT(DISTINCT l.user_id) AS likes_count,
    COUNT(DISTINCT c.id) AS comments_count,
    (COUNT(DISTINCT l.user_id) + COUNT(DISTINCT c.id) * 2) AS popularity_score
FROM posts p
JOIN users u ON p.user_id = u.id
LEFT JOIN likes l ON p.id = l.post_id
LEFT JOIN comments c ON p.id = c.post_id
GROUP BY p.id, u.username, p.content
ORDER BY popularity_score DESC;

-- 4. Follower Home Feed for User 1
-- Shows posts created by people user 1 follows, sorted chronologically
SELECT 
    p.id AS post_id,
    u.username AS author,
    p.content,
    p.created_at
FROM follows f
JOIN posts p ON f.following_id = p.user_id
JOIN users u ON p.user_id = u.id
WHERE f.follower_id = 1
ORDER BY p.created_at DESC;

-- 5. Lurker Detection (Users with zero posts, comments, or likes)
SELECT u.id, u.username, u.created_at
FROM users u
WHERE NOT EXISTS (SELECT 1 FROM posts p WHERE p.user_id = u.id)
  AND NOT EXISTS (SELECT 1 FROM comments c WHERE c.user_id = u.id)
  AND NOT EXISTS (SELECT 1 FROM likes l WHERE l.user_id = u.id)
ORDER BY u.id ASC;
