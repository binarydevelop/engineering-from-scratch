#!/usr/bin/env bash
# phases/28-container-debugging-without-magic/lab-05-permissions-mount/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"
CODE_DIR="$LESSON_DIR/code"
TEST_MOUNT="/tmp/dfs_lab05_restricted_dir"

echo "=== Running Phase 28 Lab 05: Permission Denied on Mount ==="

# Cleanup prior test dir
rm -rf "$TEST_MOUNT"
mkdir -p "$TEST_MOUNT"
# Set restrictive permissions: readable and executable only, not writable by UID 10001
chmod 755 "$TEST_MOUNT"

echo "Step 1: Running non-root container (UID 10001) mounting host dir with 755 permissions..."
set +e
docker run --rm --user 10001:10001 \
    -v "$TEST_MOUNT":/data \
    -v "$CODE_DIR/writer.py":/writer.py \
    python:3.11-slim python3 /writer.py
RUN_EXIT=$?
set -e
echo "Exit code: $RUN_EXIT (Permission denied!)"

echo ""
echo "Step 2: Systematic Diagnostics:"
echo "a. What user is running inside the container? (UID 10001)"
echo "b. What permissions exist on the mounted host directory?"
ls -ld "$TEST_MOUNT"
echo "--> DIAGNOSIS: Mounted folder is owned by host user with mode 755; UID 10001 has no write access!"

echo ""
echo "Step 3: Applying FIX (granting write access to directory)..."
chmod 777 "$TEST_MOUNT"

echo "Step 4: Rerunning container after permission fix:"
docker run --rm --user 10001:10001 \
    -v "$TEST_MOUNT":/data \
    -v "$CODE_DIR/writer.py":/writer.py \
    python:3.11-slim python3 /writer.py

echo "Verifying written file on host:"
cat "$TEST_MOUNT/audit.log"

# Cleanup
rm -rf "$TEST_MOUNT"

echo ""
echo "Lab 05 Completed Successfully."
