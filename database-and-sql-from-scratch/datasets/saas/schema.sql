-- SaaS Multi-Tenant Platform Schema
CREATE SCHEMA IF NOT EXISTS saas;
SET search_path TO saas, public;

DROP TABLE IF EXISTS events CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS memberships CASCADE;
DROP TABLE IF EXISTS subscriptions CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS organizations CASCADE;

CREATE TABLE organizations (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    plan_tier VARCHAR(50) NOT NULL DEFAULT 'starter' CHECK (plan_tier IN ('starter', 'pro', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE memberships (
    organization_id INT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member' CHECK (role IN ('owner', 'admin', 'member', 'billing')),
    joined_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (organization_id, user_id)
);

CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL UNIQUE REFERENCES organizations(id) ON DELETE CASCADE,
    monthly_price NUMERIC(10, 2) NOT NULL CHECK (monthly_price >= 0),
    seats_purchased INT NOT NULL DEFAULT 5 CHECK (seats_purchased > 0),
    status VARCHAR(50) NOT NULL DEFAULT 'active' CHECK (status IN ('trialing', 'active', 'past_due', 'cancelled')),
    start_date DATE NOT NULL,
    current_period_end DATE NOT NULL
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    organization_id INT NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id INT REFERENCES users(id) ON DELETE SET NULL,
    event_type VARCHAR(100) NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_events_org_created ON events(organization_id, created_at DESC);
CREATE INDEX idx_events_payload_gin ON events USING GIN (payload);
CREATE INDEX idx_memberships_user ON memberships(user_id);
