-- Social Network Seed Data
SET search_path TO social, public;

INSERT INTO users (id, username, full_name, bio, created_at) VALUES
(1, 'alex_code', 'Alex Rivera', 'Distributed systems & SQL fan', '2025-08-01 10:00:00+00'),
(2, 'beth_dev', 'Bethany Chen', 'Frontend architect & UI nerd', '2025-08-15 11:30:00+00'),
(3, 'charlie_data', 'Charlie Ross', 'Data scientist building LLMs', '2025-09-01 09:15:00+00'),
(4, 'dana_ops', 'Dana Vance', 'Kubernetes, SRE, on-call survivor', '2025-09-20 14:00:00+00'),
(5, 'evan_sec', 'Evan Wright', 'Security researcher & buffer overflow hunter', '2025-10-05 16:45:00+00'),
(6, 'fiona_pm', 'Fiona Gallagher', 'Product manager shipping infra', '2025-11-01 08:30:00+00'),
(7, 'quiet_luke', 'Luke Sky', 'Lurker account with zero activity', '2025-12-01 12:00:00+00');

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

INSERT INTO posts (id, user_id, content, created_at) VALUES
(1, 1, 'Why B-Tree indexes beat Sequential Scans for selective lookups.', '2026-01-05 10:00:00+00'),
(2, 1, 'PostgreSQL 16 MVCC tuple header walkthrough.', '2026-01-12 15:30:00+00'),
(3, 2, 'Tailwind CSS vs Vanilla CSS performance benchmarks.', '2026-01-15 11:00:00+00'),
(4, 3, 'Fine-tuning small language models on synthetic SQL query logs.', '2026-02-01 14:20:00+00'),
(5, 4, 'Our incident retrospective: Why a missing foreign key index locked the database.', '2026-02-10 09:45:00+00'),
(6, 1, 'Building a mini-relational engine in pure Python.', '2026-02-20 16:00:00+00'),
(7, 5, 'Common SQL injection bypass patterns in ORM abstraction layers.', '2026-03-01 13:15:00+00'),
(8, 6, 'Infra roadmap for Q2: Latency SLIs and connection pooling.', '2026-03-05 10:30:00+00');

SELECT setval('posts_id_seq', (SELECT MAX(id) FROM posts));

-- Follows (including mutual follow relationships: 1 <-> 2, 1 <-> 4)
INSERT INTO follows (follower_id, following_id, created_at) VALUES
(1, 2, '2025-08-20 10:00:00+00'),
(2, 1, '2025-08-21 14:00:00+00'), -- mutual
(1, 3, '2025-09-05 09:00:00+00'),
(1, 4, '2025-09-25 11:00:00+00'),
(4, 1, '2025-09-26 15:00:00+00'), -- mutual
(2, 3, '2025-09-10 16:00:00+00'),
(3, 1, '2025-09-15 12:00:00+00'),
(4, 5, '2025-10-10 10:30:00+00'),
(5, 1, '2025-10-12 11:45:00+00'),
(6, 1, '2025-11-05 14:10:00+00'),
(6, 4, '2025-11-06 09:20:00+00');

-- Comments
INSERT INTO comments (id, post_id, user_id, comment_text, created_at) VALUES
(1, 1, 2, 'Great explanation! What about composite index column ordering?', '2026-01-05 10:30:00+00'),
(2, 1, 4, 'Essential reading for any backend engineer.', '2026-01-05 11:15:00+00'),
(3, 2, 5, 'The xmin/xmax tuple headers make vacuum freeze obvious.', '2026-01-12 16:00:00+00'),
(4, 5, 1, 'Nested loop joins on unindexed foreign keys are brutal.', '2026-02-10 10:05:00+00'),
(5, 5, 3, 'Bookmarking this retro.', '2026-02-10 11:40:00+00'),
(6, 6, 2, 'Looking forward to testing the mini-engine!', '2026-02-20 17:00:00+00');

SELECT setval('comments_id_seq', (SELECT MAX(id) FROM comments));

-- Likes
INSERT INTO likes (post_id, user_id, created_at) VALUES
(1, 2, '2026-01-05 10:15:00+00'),
(1, 3, '2026-01-05 10:45:00+00'),
(1, 4, '2026-01-05 11:00:00+00'),
(1, 5, '2026-01-05 12:30:00+00'),
(2, 3, '2026-01-12 16:10:00+00'),
(2, 4, '2026-01-12 16:30:00+00'),
(3, 1, '2026-01-15 11:30:00+00'),
(5, 1, '2026-02-10 10:00:00+00'),
(5, 2, '2026-02-10 10:15:00+00'),
(5, 6, '2026-02-10 12:00:00+00'),
(6, 2, '2026-02-20 16:30:00+00'),
(6, 3, '2026-02-20 17:15:00+00'),
(6, 4, '2026-02-20 18:00:00+00');
