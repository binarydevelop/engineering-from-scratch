#!/usr/bin/env bash
# phases/19-health-checks-and-dependencies/01-healthcheck-probes/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 19 Experiment: Health Checks & Dependencies ==="

# Cleanup prior container
docker rm -f dfs-hc-test >/dev/null 2>&1 || true

echo "Step 1: Building image with HEALTHCHECK definition"
docker build -t dfs-health-demo:v1 "$CODE_DIR" >/dev/null

echo ""
echo "Step 2: Starting container dfs-hc-test"
docker run -d --name dfs-hc-test -p 8080:8080 dfs-health-demo:v1 >/dev/null

echo "Immediate health inspection (within start-period):"
docker inspect dfs-hc-test --format 'Status: {{.State.Status}}, Health: {{.State.Health.Status}}'

echo ""
echo "Step 3: Waiting 4 seconds for warmup and first passing probe..."
sleep 4
HEALTH_STATE=$(docker inspect dfs-hc-test --format '{{.State.Health.Status}}')
echo "Health status after warmup: $HEALTH_STATE"
docker ps --filter "name=dfs-hc-test" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "Step 4: Injecting deliberate internal failure via /break endpoint"
curl -s http://localhost:8080/break
echo ""

echo "Step 5: Waiting 6 seconds for health check probe retries to fail..."
sleep 6
BROKEN_HEALTH=$(docker inspect dfs-hc-test --format '{{.State.Health.Status}}')
echo "Health status after failure: $BROKEN_HEALTH"
docker ps --filter "name=dfs-hc-test" --format "table {{.Names}}\t{{.Status}}"

echo ""
echo "Notice: The process is still 'Up', but Docker Engine knows it is '(unhealthy)'!"
echo "Last health check probe log:"
docker inspect dfs-hc-test --format '{{range .State.Health.Log}}{{println .Output}}{{end}}' | tail -n 2

# Cleanup
docker rm -f dfs-hc-test >/dev/null

echo ""
echo "Phase 19 Experiment Completed Successfully."
