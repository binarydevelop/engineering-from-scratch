#!/usr/bin/env bash
set -euo pipefail

echo "==> Resetting database schemas in sqllab..."

# Execute reset inside docker container or via local psql
SQL_CMD="
DROP SCHEMA IF EXISTS ecommerce CASCADE;
DROP SCHEMA IF EXISTS social CASCADE;
DROP SCHEMA IF EXISTS saas CASCADE;
DROP SCHEMA IF EXISTS banking CASCADE;
DROP SCHEMA IF EXISTS analytics CASCADE;
DROP SCHEMA IF EXISTS lab CASCADE;

CREATE SCHEMA ecommerce;
CREATE SCHEMA social;
CREATE SCHEMA saas;
CREATE SCHEMA banking;
CREATE SCHEMA analytics;
CREATE SCHEMA lab;
"

if docker ps --format '{{.Names}}' | grep -q "database-sql-scratch-db"; then
    echo "$SQL_CMD" | docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -q
    echo "==> All schemas dropped and recreated cleanly in PostgreSQL container."
elif command -v psql >/dev/null 2>&1; then
    echo "$SQL_CMD" | psql -h localhost -p 5432 -U postgres -d sqllab -q
    echo "==> All schemas dropped and recreated cleanly via local psql."
else
    echo "ERROR: PostgreSQL container is not running and local psql was not found."
    echo "Run: make up"
    exit 1
fi
