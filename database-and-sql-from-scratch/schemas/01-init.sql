-- Auto-initialization entrypoint for PostgreSQL Docker container
-- Creates all base schemas

CREATE SCHEMA IF NOT EXISTS ecommerce;
CREATE SCHEMA IF NOT EXISTS social;
CREATE SCHEMA IF NOT EXISTS saas;
CREATE SCHEMA IF NOT EXISTS banking;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS lab;

-- Grant search path access
ALTER DATABASE sqllab SET search_path TO ecommerce, social, saas, banking, analytics, public;
