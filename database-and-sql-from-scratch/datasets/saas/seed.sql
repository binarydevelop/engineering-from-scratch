-- SaaS Multi-Tenant Seed Data
SET search_path TO saas, public;

INSERT INTO organizations (id, name, slug, plan_tier, created_at) VALUES
(1, 'Acme Corp', 'acme-corp', 'enterprise', '2025-06-01 08:00:00+00'),
(2, 'Beta Dynamics', 'beta-dyn', 'pro', '2025-07-15 10:00:00+00'),
(3, 'CloudFlow Labs', 'cloudflow', 'starter', '2025-09-01 12:00:00+00'),
(4, 'DataForge Inc', 'dataforge', 'enterprise', '2025-10-10 14:00:00+00'),
(5, 'Echo Security', 'echosec', 'pro', '2025-11-01 09:00:00+00'),
(6, 'Fractal Zero', 'fractal-zero', 'starter', '2026-01-15 11:30:00+00'); -- Inactive trial

SELECT setval('organizations_id_seq', (SELECT MAX(id) FROM organizations));

INSERT INTO users (id, email, full_name, created_at) VALUES
(1, 'alice@acme.com', 'Alice Martin', '2025-06-01 08:05:00+00'),
(2, 'bob@acme.com', 'Bob Vance', '2025-06-02 09:00:00+00'),
(3, 'charlie@acme.com', 'Charlie Kelly', '2025-06-15 10:00:00+00'),
(4, 'dana@beta.com', 'Dana Scully', '2025-07-15 10:10:00+00'),
(5, 'fox@beta.com', 'Fox Mulder', '2025-07-16 11:00:00+00'),
(6, 'ed@cloudflow.io', 'Ed Norton', '2025-09-01 12:05:00+00'),
(7, 'sarah@dataforge.com', 'Sarah Connor', '2025-10-10 14:05:00+00'),
(8, 'john@dataforge.com', 'John Connor', '2025-10-12 15:00:00+00'),
(9, 'kyle@dataforge.com', 'Kyle Reese', '2025-10-15 09:30:00+00'),
(10, 'marcus@dataforge.com', 'Marcus Wright', '2025-11-01 10:00:00+00'),
(11, 'grace@echosec.io', 'Grace Hopper', '2025-11-01 09:10:00+00');

SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));

-- Memberships
INSERT INTO memberships (organization_id, user_id, role, joined_at) VALUES
(1, 1, 'owner', '2025-06-01 08:05:00+00'),
(1, 2, 'admin', '2025-06-02 09:00:00+00'),
(1, 3, 'member', '2025-06-15 10:00:00+00'),
(2, 4, 'owner', '2025-07-15 10:10:00+00'),
(2, 5, 'member', '2025-07-16 11:00:00+00'),
(3, 6, 'owner', '2025-09-01 12:05:00+00'),
(4, 7, 'owner', '2025-10-10 14:05:00+00'),
(4, 8, 'admin', '2025-10-12 15:00:00+00'),
(4, 9, 'member', '2025-10-15 09:30:00+00'),
(4, 10, 'member', '2025-11-01 10:00:00+00'),
(5, 11, 'owner', '2025-11-01 09:10:00+00');

-- Subscriptions (MRR calculation facts)
INSERT INTO subscriptions (id, organization_id, monthly_price, seats_purchased, status, start_date, current_period_end) VALUES
(1, 1, 999.00, 25, 'active', '2025-06-01', '2026-06-01'),
(2, 2, 299.00, 10, 'active', '2025-07-15', '2026-07-15'),
(3, 3, 49.00, 3, 'active', '2025-09-01', '2026-09-01'),
(4, 4, 1499.00, 50, 'active', '2025-10-10', '2026-10-10'),
(5, 5, 299.00, 10, 'past_due', '2025-11-01', '2026-04-01'),
(6, 6, 0.00, 2, 'trialing', '2026-01-15', '2026-02-15');

SELECT setval('subscriptions_id_seq', (SELECT MAX(id) FROM subscriptions));

-- Projects
INSERT INTO projects (id, organization_id, name, is_active, created_at) VALUES
(1, 1, 'Core Infrastructure Migration', TRUE, '2025-06-10 10:00:00+00'),
(2, 1, 'Data Warehouse ETL', TRUE, '2025-07-01 11:00:00+00'),
(3, 2, 'Web Portal Redesign', TRUE, '2025-08-01 14:00:00+00'),
(4, 3, 'Microservices Gateway', TRUE, '2025-09-15 09:30:00+00'),
(5, 4, 'Cybernetic Defense System', TRUE, '2025-10-20 16:00:00+00'),
(6, 4, 'Neural Net Training Pipeline', TRUE, '2025-11-05 13:00:00+00');

SELECT setval('projects_id_seq', (SELECT MAX(id) FROM projects));

-- Events (Activity logs with JSONB payloads)
INSERT INTO events (organization_id, user_id, event_type, payload, created_at) VALUES
(1, 1, 'deploy.started', '{"env": "prod", "version": "v1.2.0"}'::jsonb, '2026-01-10 10:00:00+00'),
(1, 1, 'deploy.succeeded', '{"env": "prod", "duration_sec": 42}'::jsonb, '2026-01-10 10:01:00+00'),
(1, 2, 'export.generated', '{"format": "csv", "row_count": 150000}'::jsonb, '2026-01-15 14:30:00+00'),
(2, 4, 'settings.updated', '{"feature_flags": {"dark_mode": true}}'::jsonb, '2026-01-18 11:00:00+00'),
(4, 7, 'compute.cluster_spawned', '{"nodes": 8, "gpu": "h100"}'::jsonb, '2026-02-01 09:00:00+00'),
(4, 8, 'compute.job_finished', '{"job_id": 992, "exit_code": 0}'::jsonb, '2026-02-01 15:45:00+00'),
(1, 3, 'api.rate_limited', '{"endpoint": "/v1/metrics", "burst": 500}'::jsonb, '2026-02-15 18:20:00+00'),
(3, 6, 'user.login', '{"ip": "192.168.1.1", "device": "macOS"}'::jsonb, '2026-02-20 08:30:00+00'),
(4, 9, 'compute.job_failed', '{"job_id": 1045, "error": "CUDA out of memory"}'::jsonb, '2026-03-01 12:10:00+00');
