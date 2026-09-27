#!/usr/bin/env bash
# phases/21-what-actually-happens-during-compose-up/01-execution-dag-and-reconciliation/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 21 Experiment: Tracing docker compose up ==="

# Cleanup prior state
docker compose -f "$CODE_DIR/compose.yaml" down -v >/dev/null 2>&1 || true

echo "Step 1: Inspecting Variable Interpolation via 'docker compose config'"
docker compose -f "$CODE_DIR/compose.yaml" config | grep -E "image:|ports:|POSTGRES_PASSWORD:"

echo ""
echo "Step 2: Starting background Docker daemon event tracer..."
docker events --format 'EVENT: type={{.Type}} action={{.Action}} name={{.Actor.Attributes.name}}' > /tmp/dfs_compose_trace.log 2>&1 &
TRACER_PID=$!
sleep 0.5

echo ""
echo "Step 3: Executing 'docker compose up -d'..."
docker compose -f "$CODE_DIR/compose.yaml" up -d --wait

sleep 1
kill "$TRACER_PID" 2>/dev/null || true

echo ""
echo "Step 4: Observed Docker Engine API Event Sequence:"
echo "--------------------------------------------------------"
cat /tmp/dfs_compose_trace.log | grep -E "type=(network|volume|container)" || true
echo "--------------------------------------------------------"

echo ""
echo "Step 5: Verifying concrete existence of each resource:"
echo "1. Network: $(docker network ls --filter name=dfs-trace-project_backend --format '{{.Name}} (ID: {{.ID}})')"
echo "2. Volume:  $(docker volume ls --filter name=dfs-trace-project_pg-storage --format '{{.Name}}')"
echo "3. Containers:"
docker compose -f "$CODE_DIR/compose.yaml" ps

# Cleanup
rm -f /tmp/dfs_compose_trace.log
docker compose -f "$CODE_DIR/compose.yaml" down -v >/dev/null

echo ""
echo "Phase 21 Experiment Completed Successfully."
