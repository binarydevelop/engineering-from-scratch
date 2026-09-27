-- Clickstream & Event Analytics Schema
CREATE SCHEMA IF NOT EXISTS analytics;
SET search_path TO analytics, public;

DROP TABLE IF EXISTS user_cohorts CASCADE;
DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS campaigns CASCADE;

CREATE TABLE campaigns (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    utm_source VARCHAR(50) NOT NULL,
    utm_medium VARCHAR(50) NOT NULL,
    budget NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id INT NOT NULL,
    campaign_id INT REFERENCES campaigns(id),
    device_type VARCHAR(20) NOT NULL CHECK (device_type IN ('mobile', 'desktop', 'tablet')),
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ
);

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    user_id INT NOT NULL,
    event_name VARCHAR(50) NOT NULL CHECK (event_name IN ('page_view', 'sign_up', 'view_product', 'add_to_cart', 'begin_checkout', 'purchase')),
    url_path VARCHAR(255) NOT NULL,
    event_timestamp TIMESTAMPTZ NOT NULL
);

CREATE TABLE user_cohorts (
    user_id INT PRIMARY KEY,
    cohort_month DATE NOT NULL,
    first_seen_at TIMESTAMPTZ NOT NULL
);

CREATE INDEX idx_events_user_timestamp ON events(user_id, event_timestamp);
CREATE INDEX idx_events_name_time ON events(event_name, event_timestamp);
CREATE INDEX idx_sessions_user_start ON sessions(user_id, started_at);
