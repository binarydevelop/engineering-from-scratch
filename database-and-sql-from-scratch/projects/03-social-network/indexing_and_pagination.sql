-- Social Feed Indexing and Keyset Cursor Pagination
SET search_path TO social, public;

-- Scenario: Feed pagination for user 1
-- 1. Inefficient Approach: OFFSET Pagination
-- As OFFSET increases to 10,000, PostgreSQL must scan and discard 10,000 rows!
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.id, p.user_id, p.content, p.created_at
FROM follows f
JOIN posts p ON f.following_id = p.user_id
WHERE f.follower_id = 1
ORDER BY p.created_at DESC, p.id DESC
LIMIT 5 OFFSET 0;

-- 2. Production Approach: Keyset Cursor Pagination
-- Pass the timestamp and ID of the last seen post as a tuple cursor (created_at, id) < ($last_time, $last_id)
-- Runs in constant O(log N) time regardless of depth!
EXPLAIN (ANALYZE, BUFFERS)
SELECT p.id, p.user_id, p.content, p.created_at
FROM follows f
JOIN posts p ON f.following_id = p.user_id
WHERE f.follower_id = 1
  AND (p.created_at, p.id) < ('2026-02-01 14:20:00+00'::TIMESTAMPTZ, 4)
ORDER BY p.created_at DESC, p.id DESC
LIMIT 5;

-- 3. Composite Index for Timeline Lookups
CREATE INDEX IF NOT EXISTS idx_posts_user_timeline 
ON posts (user_id, created_at DESC, id DESC);
