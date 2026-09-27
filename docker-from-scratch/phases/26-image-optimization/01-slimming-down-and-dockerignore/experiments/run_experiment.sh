#!/usr/bin/env bash
# phases/26-image-optimization/01-slimming-down-and-dockerignore/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"

echo "=== Running Phase 26 Experiment: Image Optimization ==="

echo "Step 1: Generating temporary 20MB host asset: large_asset.bin..."
dd if=/dev/zero of="$CODE_DIR/large_asset.bin" bs=1M count=20 2>/dev/null

echo ""
echo "Step 2: Building BLOATED image without .dockerignore..."
# Temporarily disable .dockerignore to demonstrate context explosion
mv "$CODE_DIR/.dockerignore" "$CODE_DIR/.dockerignore.bak"
docker build -f "$CODE_DIR/Dockerfile.bloated" -t dfs-opt-bloated:v1 "$CODE_DIR" >/dev/null
mv "$CODE_DIR/.dockerignore.bak" "$CODE_DIR/.dockerignore"

echo ""
echo "Step 3: Building OPTIMIZED image with .dockerignore and minimal base..."
docker build -f "$CODE_DIR/Dockerfile.optimized" -t dfs-opt-lean:v1 "$CODE_DIR" >/dev/null

echo ""
echo "Step 4: Comparing image sizes on disk:"
echo "----------------------------------------------------------------------"
docker images --filter "reference=dfs-opt-*" --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo "----------------------------------------------------------------------"

echo ""
echo "Step 5: Proving why 'RUN rm -rf' in a separate layer is an illusion:"
echo "Inspecting layer history of bloated image:"
docker history dfs-opt-bloated:v1 | head -n 4
echo "Notice: The 15MB file created in step 4 still occupies 15MB in that layer,"
echo "even though step 5 deleted it from the merged view!"

# Cleanup
rm -f "$CODE_DIR/large_asset.bin"
docker rmi -f dfs-opt-bloated:v1 dfs-opt-lean:v1 >/dev/null 2>&1 || true

echo ""
echo "Phase 26 Experiment Completed Successfully."
