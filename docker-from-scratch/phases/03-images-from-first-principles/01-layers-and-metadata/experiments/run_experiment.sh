#!/usr/bin/env bash
# phases/03-images-from-first-principles/01-layers-and-metadata/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 03 Experiment: Images From First Principles ==="

echo "Step 1: Verifying base image 'alpine:latest'"
if ! docker image inspect alpine:latest >/dev/null 2>&1; then
    docker pull alpine:latest
else
    echo "Image 'alpine:latest' is already available locally."
fi

echo ""
echo "Step 2: Inspecting alpine image layers and metadata"
python3 "$LESSON_DIR/code/inspect_image_layers.py" alpine:latest

echo ""
echo "Step 3: Comparing image sizes and history"
docker images alpine:latest
docker history alpine:latest

echo ""
echo "Step 4: Demonstrating image immutability (tagging vs copying)"
# Creating a new tag does not duplicate layers or data on disk
docker tag alpine:latest dfs-alpine-tag:v1
ALPINE_ORIG_ID=$(docker inspect alpine:latest --format '{{.Id}}')
ALPINE_TAG_ID=$(docker inspect dfs-alpine-tag:v1 --format '{{.Id}}')
echo "Original Image ID: $ALPINE_ORIG_ID"
echo "Tagged Image ID:   $ALPINE_TAG_ID"
if [ "$ALPINE_ORIG_ID" = "$ALPINE_TAG_ID" ]; then
    echo "Confirmed: Tags are mutable pointers to identical immutable image IDs."
fi

# Clean up temporary tag
docker rmi dfs-alpine-tag:v1 >/dev/null

echo ""
echo "Phase 03 Experiment Completed Successfully."
