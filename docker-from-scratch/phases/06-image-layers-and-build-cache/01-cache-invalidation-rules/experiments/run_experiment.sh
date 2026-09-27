#!/usr/bin/env bash
# phases/06-image-layers-and-build-cache/01-cache-invalidation-rules/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 06 Experiment: Image Layers & Build Cache ==="

echo "--- Experiment A: The Naive Dockerfile ---"
echo "A1: Initial build of Naive Dockerfile (Expect ~3s build)..."
START_TIME=$(date +%s)
docker build -f "$CODE_DIR/Dockerfile.naive" -t dfs-cache-naive:v1 "$CODE_DIR" >/dev/null
DURATION=$(( $(date +%s) - START_TIME ))
echo "Naive initial build took: ${DURATION}s"

echo "A2: Modifying app.py (high-volatility code change)..."
echo "# modified at $(date)" >> "$CODE_DIR/app.py"

echo "A3: Rebuilding Naive Dockerfile after code change..."
START_TIME=$(date +%s)
docker build -f "$CODE_DIR/Dockerfile.naive" -t dfs-cache-naive:v2 "$CODE_DIR"
DURATION=$(( $(date +%s) - START_TIME ))
echo "Naive rebuild took: ${DURATION}s (Cache was completely busted!)"

echo ""
echo "--- Experiment B: The Optimized Dependency-Aware Dockerfile ---"
echo "B1: Initial build of Optimized Dockerfile (Expect ~3s build)..."
START_TIME=$(date +%s)
docker build -f "$CODE_DIR/Dockerfile.optimized" -t dfs-cache-opt:v1 "$CODE_DIR" >/dev/null
DURATION=$(( $(date +%s) - START_TIME ))
echo "Optimized initial build took: ${DURATION}s"

echo "B2: Modifying app.py again..."
echo "# modified again at $(date)" >> "$CODE_DIR/app.py"

echo "B3: Rebuilding Optimized Dockerfile after code change..."
START_TIME=$(date +%s)
docker build -f "$CODE_DIR/Dockerfile.optimized" -t dfs-cache-opt:v2 "$CODE_DIR"
DURATION=$(( $(date +%s) - START_TIME ))
echo "Optimized rebuild took: ${DURATION}s (Dependency layer was CACHED!)"

echo ""
echo "B4: Intentionally busting cache by modifying requirements.txt..."
echo "# dependency update $(date)" >> "$CODE_DIR/requirements.txt"
START_TIME=$(date +%s)
docker build -f "$CODE_DIR/Dockerfile.optimized" -t dfs-cache-opt:v3 "$CODE_DIR" >/dev/null
DURATION=$(( $(date +%s) - START_TIME ))
echo "Rebuild after dependency change took: ${DURATION}s (Cache properly invalidated)"

# Reset app.py and requirements.txt
git checkout -- "$CODE_DIR/app.py" "$CODE_DIR/requirements.txt" 2>/dev/null || true

echo ""
echo "Phase 06 Experiment Completed Successfully."
