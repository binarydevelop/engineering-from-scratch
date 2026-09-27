#!/usr/bin/env bash
# Production Backup & Verification Engine
set -euo pipefail

SOURCE_DIR="${1:-/tmp/lfs-lab/data}"
BACKUP_ROOT="${2:-/tmp/lfs-lab/backups}"
RETENTION_COUNT=5

mkdir -p "$BACKUP_ROOT"
mkdir -p "$SOURCE_DIR"

# Populate mock data if empty
if [ -z "$(ls -A "$SOURCE_DIR")" ]; then
    echo "Sample data generated on $(date)" > "$SOURCE_DIR/sample.txt"
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_FILE="$BACKUP_ROOT/backup_${TIMESTAMP}.tar.gz"

echo "[*] Creating compressed archive: $ARCHIVE_FILE..."
tar -czf "$ARCHIVE_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

echo "[*] Generating cryptographic checksum..."
sha256sum "$ARCHIVE_FILE" > "${ARCHIVE_FILE}.sha256"

echo "[*] Executing test restoration drill into isolated sandbox..."
RESTORE_TMP=$(mktemp -d /tmp/lfs-restore.XXXXXX)
trap 'rm -rf "$RESTORE_TMP"' EXIT

tar -xzf "$ARCHIVE_FILE" -C "$RESTORE_TMP"
if [ -f "$RESTORE_TMP/$(basename "$SOURCE_DIR")/sample.txt" ]; then
    echo "[✓] Restoration verification passed."
else
    echo "[✗] Restoration verification FAILED."
    exit 1
fi

echo "[*] Pruning old archives, keeping latest $RETENTION_COUNT..."
cd "$BACKUP_ROOT"
# shellcheck disable=SC2012
ls -t backup_*.tar.gz | tail -n +$((RETENTION_COUNT + 1)) | while read -r old_tar; do
    echo "  Pruning: $old_tar"
    rm -f "$old_tar" "${old_tar}.sha256"
done

echo "[✓] Backup cycle completed successfully."
