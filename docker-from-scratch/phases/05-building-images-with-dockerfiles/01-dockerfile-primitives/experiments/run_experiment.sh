#!/usr/bin/env bash
# phases/05-building-images-with-dockerfiles/01-dockerfile-primitives/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 05 Experiment: Building Images with Dockerfiles ==="

# Cleanup prior test container if any
docker rm -f dfs-app-test >/dev/null 2>&1 || true

echo "Step 1: Building image from Dockerfile (docker build)"
docker build -t dfs-custom-app:v1 "$LESSON_DIR/code"

echo ""
echo "Step 2: Inspecting created image history and metadata"
docker history dfs-custom-app:v1
docker image inspect dfs-custom-app:v1 --format 'CMD: {{json .Config.Cmd}}, WorkDir: {{.Config.WorkingDir}}, Env: {{json .Config.Env}}'

echo ""
echo "Step 3: Running container from custom image"
docker run -d --name dfs-app-test -p 8000:8000 -e SERVICE_NAME="alpha-service" dfs-custom-app:v1

sleep 1

echo ""
echo "Step 4: Testing HTTP response from containerized application"
curl -s http://localhost:8000
echo ""

echo ""
echo "Step 5: Inspecting container logs"
docker logs dfs-app-test

# Cleanup
docker rm -f dfs-app-test >/dev/null
echo ""
echo "Phase 05 Experiment Completed Successfully."
