#!/usr/bin/env bash
# phases/04-containers-and-filesystems/01-copy-on-write-layer/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 04 Experiment: Containers and Filesystems ==="

echo "Step 1: Running python test_cow_isolation.py"
python3 "$LESSON_DIR/code/test_cow_isolation.py"

echo ""
echo "Step 2: Inspecting Storage Driver and Filesystem mutations"
docker rm -f dfs-driver-inspect >/dev/null 2>&1 || true
docker run -d --name dfs-driver-inspect alpine:latest sleep 10 >/dev/null
echo "Storage Driver: $(docker inspect dfs-driver-inspect --format '{{.Driver}}')"
docker exec dfs-driver-inspect touch /tmp/new_file.txt
echo "Mutations in container writable layer (docker diff):"
docker diff dfs-driver-inspect
docker rm -f dfs-driver-inspect >/dev/null

echo ""
echo "Phase 04 Experiment Completed Successfully."
