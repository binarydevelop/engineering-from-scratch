#!/usr/bin/env bash
# phases/27-multi-stage-builds/01-builder-pattern-and-minimal-runtime/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 27 Experiment: Multi-Stage Builds ==="

echo "Step 1: Building Single-Stage Image (Build tools embedded in runtime)..."
docker build -f "$CODE_DIR/Dockerfile.single" -t dfs-single:v1 "$CODE_DIR" >/dev/null

echo ""
echo "Step 2: Building Multi-Stage Image (Build tools stripped from runtime)..."
docker build -f "$CODE_DIR/Dockerfile.multistage" -t dfs-multi:v1 "$CODE_DIR" >/dev/null

echo ""
echo "Step 3: Comparing Final Image Sizes:"
echo "----------------------------------------------------------------------"
docker images --filter "reference=dfs-single*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
docker images --filter "reference=dfs-multi*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo "----------------------------------------------------------------------"

echo ""
echo "Step 4: Inspecting Build Debris in Single-Stage Image:"
docker run --rm dfs-single:v1 ls -lh /build/tools/compiler_suite.bin

echo ""
echo "Step 5: Verifying Build Debris is GONE in Multi-Stage Image:"
set +e
docker run --rm dfs-multi:v1 ls -lh /build 2>&1
DEBRIS_EXIT=$?
set -e
if [ "$DEBRIS_EXIT" -ne 0 ]; then
    echo "--> VERIFIED: /build directory does not even exist in the multi-stage runtime image!"
fi

echo ""
echo "Step 6: Verifying Application Execution in Both Images:"
echo "[Single-Stage Output]:"
docker run --rm dfs-single:v1
echo "[Multi-Stage Output]:"
docker run --rm dfs-multi:v1

# Cleanup
docker rmi -f dfs-single:v1 dfs-multi:v1 >/dev/null 2>&1 || true

echo ""
echo "Phase 27 Experiment Completed Successfully."
