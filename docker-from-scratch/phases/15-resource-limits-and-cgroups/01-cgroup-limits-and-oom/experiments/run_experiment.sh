#!/usr/bin/env bash
# phases/15-resource-limits-and-cgroups/01-cgroup-limits-and-oom/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 15 Experiment: Resource Limits & cgroups ==="

# Cleanup prior container
docker rm -f dfs-oom-test dfs-cpu-test >/dev/null 2>&1 || true

echo "Step 1: Running container with strict 50MB memory limit (-m 50m --memory-swap 50m)"
set +e
docker run --name dfs-oom-test \
    -m 50m --memory-swap 50m \
    -v "$CODE_DIR/memory_hog.py":/memory_hog.py \
    python:3.11-slim python3 /memory_hog.py
RUN_EXIT=$?
set -e

echo ""
echo "Step 2: Inspecting container exit status"
echo "Process exit code: $RUN_EXIT (Notice: 137 = 128 + 9 SIGKILL)"

echo ""
echo "Step 3: Querying Docker Engine for Out-Of-Memory termination evidence"
OOM_KILLED=$(docker inspect dfs-oom-test --format '{{.State.OOMKilled}}')
EXIT_CODE=$(docker inspect dfs-oom-test --format '{{.State.ExitCode}}')
echo "Container State.OOMKilled: $OOM_KILLED"
echo "Container State.ExitCode:  $EXIT_CODE"

if [ "$OOM_KILLED" = "true" ]; then
    echo "--> VERIFIED: Linux cgroup memory controller triggered kernel OOM-killer!"
fi

echo ""
echo "Step 4: Demonstrating CPU Throttling limit (--cpus 0.5)"
docker run -d --name dfs-cpu-test --cpus 0.5 alpine:latest sh -c "while true; do :; done" >/dev/null
echo "Container dfs-cpu-test launched with 0.5 CPU limit."
echo "Active resource stats (single sample via docker stats):"
docker stats --no-stream dfs-cpu-test --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}"

# Cleanup
docker rm -f dfs-oom-test dfs-cpu-test >/dev/null

echo ""
echo "Phase 15 Experiment Completed Successfully."
