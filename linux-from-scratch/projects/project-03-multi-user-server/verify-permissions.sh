#!/usr/bin/env bash
# Verification of SGID Directory Behavior
set -euo pipefail

SHARED_DIR="/tmp/lfs-lab/projects/core"
TEST_FILE="$SHARED_DIR/test_artifact_$(date +%s).txt"

echo "[*] Creating test file inside SGID directory: $TEST_FILE..."
touch "$TEST_FILE"

FILE_GROUP=$(stat -c "%G" "$TEST_FILE")
DIR_GROUP=$(stat -c "%G" "$SHARED_DIR")

echo "  Directory Group Owner: $DIR_GROUP"
echo "  Created File Group   : $FILE_GROUP"

if [ "$FILE_GROUP" = "$DIR_GROUP" ]; then
    echo "[✓] SUCCESS: SGID bit successfully inherited group ownership!"
else
    echo "[✗] FAILURE: File group ($FILE_GROUP) does not match directory ($DIR_GROUP)"
    exit 1
fi

rm -f "$TEST_FILE"
