-- Clickstream & Event Analytics Seed Data
SET search_path TO analytics, public;

INSERT INTO campaigns (id, name, utm_source, utm_medium, budget, created_at) VALUES
(1, 'New Year Tech Kickoff', 'google', 'cpc', 5000.00, '2025-12-20 00:00:00+00'),
(2, 'Developer Newsletter Sponsorship', 'newsletter', 'email', 1500.00, '2026-01-01 00:00:00+00'),
(3, 'Organic Social Campaign', 'twitter', 'social', 0.00, '2026-01-15 00:00:00+00');

SELECT setval('campaigns_id_seq', (SELECT MAX(id) FROM campaigns));

-- Cohorts: Users 101 to 105 in Jan 2026 cohort; Users 106 to 110 in Feb 2026 cohort
INSERT INTO user_cohorts (user_id, cohort_month, first_seen_at) VALUES
(101, '2026-01-01', '2026-01-02 10:00:00+00'),
(102, '2026-01-01', '2026-01-03 11:30:00+00'),
(103, '2026-01-01', '2026-01-05 14:00:00+00'),
(104, '2026-01-01', '2026-01-10 09:15:00+00'),
(105, '2026-01-01', '2026-01-15 16:20:00+00'),
(106, '2026-02-01', '2026-02-01 08:30:00+00'),
(107, '2026-02-01', '2026-02-04 12:45:00+00'),
(108, '2026-02-01', '2026-02-10 15:00:00+00'),
(109, '2026-02-01', '2026-02-14 10:10:00+00'),
(110, '2026-02-01', '2026-02-20 17:30:00+00');

-- Sessions
INSERT INTO sessions (id, user_id, campaign_id, device_type, started_at, ended_at) VALUES
('b0000000-0000-0000-0000-000000000001', 101, 1, 'desktop', '2026-01-02 10:00:00+00', '2026-01-02 10:25:00+00'),
('b0000000-0000-0000-0000-000000000002', 102, 1, 'mobile',  '2026-01-03 11:30:00+00', '2026-01-03 11:45:00+00'),
('b0000000-0000-0000-0000-000000000003', 103, 2, 'desktop', '2026-01-05 14:00:00+00', '2026-01-05 14:10:00+00'),
('b0000000-0000-0000-0000-000000000004', 104, 3, 'mobile',  '2026-01-10 09:15:00+00', '2026-01-10 09:40:00+00'),
('b0000000-0000-0000-0000-000000000005', 101, NULL, 'desktop', '2026-02-05 11:00:00+00', '2026-02-05 11:30:00+00'), -- User 101 retained in Feb
('b0000000-0000-0000-0000-000000000006', 102, NULL, 'mobile',  '2026-02-08 14:20:00+00', '2026-02-08 14:50:00+00'), -- User 102 retained in Feb
('b0000000-0000-0000-0000-000000000007', 106, 1, 'desktop', '2026-02-01 08:30:00+00', '2026-02-01 08:55:00+00'),
('b0000000-0000-0000-0000-000000000008', 107, 2, 'mobile',  '2026-02-04 12:45:00+00', '2026-02-04 13:00:00+00');

-- Funnel & Activity Events
-- User 101: Complete purchase funnel
INSERT INTO events (session_id, user_id, event_name, url_path, event_timestamp) VALUES
('b0000000-0000-0000-0000-000000000001', 101, 'page_view',      '/',                        '2026-01-02 10:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'sign_up',        '/register',                '2026-01-02 10:05:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'view_product',   '/products/ultrabook-pro',  '2026-01-02 10:10:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'add_to_cart',    '/cart/add',                '2026-01-02 10:12:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'begin_checkout', '/checkout',                '2026-01-02 10:15:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'purchase',       '/checkout/success',        '2026-01-02 10:20:00+00');

-- User 102: Drops off after add_to_cart
INSERT INTO events (session_id, user_id, event_name, url_path, event_timestamp) VALUES
('b0000000-0000-0000-0000-000000000002', 102, 'page_view',      '/',                        '2026-01-03 11:30:00+00'),
('b0000000-0000-0000-0000-000000000002', 102, 'sign_up',        '/register',                '2026-01-03 11:35:00+00'),
('b0000000-0000-0000-0000-000000000002', 102, 'view_product',   '/products/headphones-x',   '2026-01-03 11:38:00+00'),
('b0000000-0000-0000-0000-000000000002', 102, 'add_to_cart',    '/cart/add',                '2026-01-03 11:40:00+00');

-- User 103: Drops off at page_view
INSERT INTO events (session_id, user_id, event_name, url_path, event_timestamp) VALUES
('b0000000-0000-0000-0000-000000000003', 103, 'page_view',      '/landing/sale',            '2026-01-05 14:00:00+00');

-- User 104: Drops off at view_product
INSERT INTO events (session_id, user_id, event_name, url_path, event_timestamp) VALUES
('b0000000-0000-0000-0000-000000000004', 104, 'page_view',      '/',                        '2026-01-10 09:15:00+00'),
('b0000000-0000-0000-0000-000000000004', 104, 'view_product',   '/products/phone-pro',      '2026-01-10 09:25:00+00');

-- User 101 Gaps & Islands Activity: 5 consecutive days of activity in Jan (Jan 10, 11, 12, 13, 14)
INSERT INTO events (session_id, user_id, event_name, url_path, event_timestamp) VALUES
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-10 14:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-11 14:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-12 14:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-13 14:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-14 14:00:00+00'),
-- Gap on Jan 15, then 2 consecutive days:
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-16 14:00:00+00'),
('b0000000-0000-0000-0000-000000000001', 101, 'page_view', '/dashboard', '2026-01-17 14:00:00+00');
