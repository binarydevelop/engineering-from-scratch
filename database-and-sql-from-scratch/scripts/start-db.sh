#!/usr/bin/env bash
set -euo pipefail

echo "==> Starting pinned PostgreSQL 16.4 container..."
docker compose up -d postgres

echo "==> Waiting for PostgreSQL to become healthy..."
TIMEOUT=30
ELAPSED=0

until docker exec database-sql-scratch-db pg_isready -U postgres -d sqllab >/dev/null 2>&1; do
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    if [ "$ELAPSED" -ge "$TIMEOUT" ]; then
        echo "ERROR: Timed out waiting for PostgreSQL container."
        docker compose logs postgres
        exit 1
    fi
done

echo "==> PostgreSQL 16.4 is up and ready on localhost:5432 (database: sqllab, user: postgres)"
echo "    Connect anytime with: make psql"
