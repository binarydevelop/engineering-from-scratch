#!/usr/bin/env bash
# phases/07-registries-tags-pull-and-push/01-registry-manifests-and-digests/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 07 Experiment: Registries, Tags, Pull & Push ==="

echo "Step 1: Deconstructing image reference syntax and digests"
python3 "$LESSON_DIR/code/inspect_registry_manifest.py" "redis:7-alpine"

echo ""
echo "Step 2: Inspecting immutable digests vs mutable tags"
docker image inspect redis:7-alpine --format 'Image ID: {{.Id}}'
docker image inspect redis:7-alpine --format 'RepoDigests: {{json .RepoDigests}}'

echo ""
echo "Step 3: Creating a custom registry tag pointing to the same image"
docker tag redis:7-alpine registry.internal.corp:5000/infra/cache:7.4
echo "Tagged as registry.internal.corp:5000/infra/cache:7.4"

echo ""
echo "Step 4: Proving that tagging is an alias, not a data copy"
ORIG_ID=$(docker inspect redis:7-alpine --format '{{.Id}}')
NEW_ID=$(docker inspect registry.internal.corp:5000/infra/cache:7.4 --format '{{.Id}}')
if [ "$ORIG_ID" = "$NEW_ID" ]; then
    echo "Confirmed: Both image tags resolve to the exact same immutable SHA256 ID."
fi

# Cleanup tag
docker rmi registry.internal.corp:5000/infra/cache:7.4 >/dev/null

echo ""
echo "Phase 07 Experiment Completed Successfully."
