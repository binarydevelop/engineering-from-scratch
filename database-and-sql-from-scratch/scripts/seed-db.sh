#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:-all}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

run_sql_file() {
    local file_path="$1"
    local desc="$2"
    echo "    Loading $desc from $file_path..."
    if docker ps --format '{{.Names}}' | grep -q "database-sql-scratch-db"; then
        docker exec -i database-sql-scratch-db psql -U postgres -d sqllab -q < "$file_path"
    elif command -v psql >/dev/null 2>&1; then
        psql -h localhost -p 5432 -U postgres -d sqllab -q -f "$file_path"
    else
        echo "ERROR: PostgreSQL is not accessible. Run 'make up' first."
        exit 1
    fi
}

seed_dataset() {
    local dataset="$1"
    echo "==> Seeding dataset: [$dataset]"
    local schema_file="$ROOT_DIR/datasets/$dataset/schema.sql"
    local seed_file="$ROOT_DIR/datasets/$dataset/seed.sql"

    if [ -f "$schema_file" ]; then
        run_sql_file "$schema_file" "schema"
    fi
    if [ -f "$seed_file" ]; then
        run_sql_file "$seed_file" "seed data"
    fi
}

echo "======================================================================"
echo " DATABASE AND SQL FROM SCRATCH: Dataset Provisioning"
echo "======================================================================"

case "$TARGET" in
    ecommerce)
        seed_dataset "ecommerce"
        ;;
    social)
        seed_dataset "social"
        ;;
    saas)
        seed_dataset "saas"
        ;;
    banking)
        seed_dataset "banking"
        ;;
    analytics)
        seed_dataset "analytics"
        ;;
    all)
        seed_dataset "ecommerce"
        seed_dataset "social"
        seed_dataset "saas"
        seed_dataset "banking"
        seed_dataset "analytics"
        ;;
    *)
        echo "Unknown dataset target: $TARGET"
        echo "Valid targets: all | ecommerce | social | saas | banking | analytics"
        exit 1
        ;;
esac

echo "======================================================================"
echo " Seeding completed successfully for target: $TARGET"
echo "======================================================================"
