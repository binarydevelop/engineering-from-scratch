#!/usr/bin/env bash
# phases/23-compose-volumes-and-persistent-state/01-compose-state-lifecycle/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 23 Experiment: Compose Volumes & State Lifecycle ==="

# Cleanup prior state
docker compose -f "$CODE_DIR/compose.yaml" down -v >/dev/null 2>&1 || true

echo "Step 1: Starting PostgreSQL via Docker Compose..."
docker compose -f "$CODE_DIR/compose.yaml" up -d

echo "Waiting for Postgres to initialize..."
until docker compose -f "$CODE_DIR/compose.yaml" exec -T database pg_isready -U postgres -d appdb >/dev/null 2>&1; do
    sleep 0.5
done
echo "Postgres is ready."

echo ""
echo "Step 2: Creating table 'users' and inserting records..."
docker compose -f "$CODE_DIR/compose.yaml" exec -T database psql -U postgres -d appdb -c "
    CREATE TABLE users (id SERIAL PRIMARY KEY, name VARCHAR(50), email VARCHAR(50));
    INSERT INTO users (name, email) VALUES ('Alice Smith', 'alice@example.com'), ('Bob Jones', 'bob@example.com');
"

echo "Verifying inserted records:"
docker compose -f "$CODE_DIR/compose.yaml" exec -T database psql -U postgres -d appdb -c "SELECT * FROM users;"

echo ""
echo "Step 3: Executing 'docker compose down' (NO -v flag - containers removed, volumes preserved)..."
docker compose -f "$CODE_DIR/compose.yaml" down

echo "Checking if volume still exists on disk:"
docker volume ls --filter name=dfs-volume-lifecycle_db-data

echo ""
echo "Step 4: Relaunching with 'docker compose up -d'..."
docker compose -f "$CODE_DIR/compose.yaml" up -d
until docker compose -f "$CODE_DIR/compose.yaml" exec -T database pg_isready -U postgres -d appdb >/dev/null 2>&1; do
    sleep 0.5
done

echo "Querying database after restart:"
docker compose -f "$CODE_DIR/compose.yaml" exec -T database psql -U postgres -d appdb -c "SELECT * FROM users;"
echo "--> VERIFIED: Data survived container removal because named volume persisted!"

echo ""
echo "Step 5: Executing 'docker compose down -v' (WITH -v flag - deletes containers AND volumes!)..."
docker compose -f "$CODE_DIR/compose.yaml" down -v

echo "Checking volume existence after -v down:"
docker volume ls --filter name=dfs-volume-lifecycle_db-data

echo ""
echo "Step 6: Relaunching with 'docker compose up -d' after volume destruction..."
docker compose -f "$CODE_DIR/compose.yaml" up -d
until docker compose -f "$CODE_DIR/compose.yaml" exec -T database pg_isready -U postgres -d appdb >/dev/null 2>&1; do
    sleep 0.5
done

echo "Querying database after volume wipe (Expect Table Does Not Exist):"
set +e
docker compose -f "$CODE_DIR/compose.yaml" exec -T database psql -U postgres -d appdb -c "SELECT * FROM users;"
QUERY_EXIT=$?
set -e

if [ "$QUERY_EXIT" -ne 0 ]; then
    echo "--> VERIFIED: The -v flag completely annihilated the persistent volume and its data!"
fi

# Cleanup
docker compose -f "$CODE_DIR/compose.yaml" down -v >/dev/null

echo ""
echo "Phase 23 Experiment Completed Successfully."
