#!/usr/bin/env bash
set -euo pipefail

echo "==> Stopping PostgreSQL 16.4 container..."
docker compose down
echo "==> Database container stopped."
