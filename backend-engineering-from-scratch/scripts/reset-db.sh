#!/usr/bin/env bash
set -euo pipefail

echo "Resetting local development databases and SQLite test files..."

find . -type f -name "*.db" -delete
find . -type f -name "*.sqlite3" -delete
find . -type f -name "*.db-journal" -delete
find . -type f -name "*.db-wal" -delete
find . -type f -name "*.db-shm" -delete

echo "Local database files cleared."
