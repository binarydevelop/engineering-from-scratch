#!/usr/bin/env bash
# Production Incremental Backup & Rotation Utility
# Demonstrates tar, gzip, sha256 checksums, and retention pruning
set -euo pipefail

SOURCE_DIR="${1:-/tmp/lfs-lab/data}"
BACKUP_DIR="${2:-/tmp/lfs-lab/backups}"
RETENTION_DAYS=7

mkdir -p "$BACKUP_DIR"

if [ ! -d "$SOURCE_DIR" ]; then
    echo "ERROR: Source directory $SOURCE_DIR does not exist." >&2
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_NAME="backup_${TIMESTAMP}.tar.gz"
TARGET_FILE="${BACKUP_DIR}/${ARCHIVE_NAME}"

echo "[*] Creating compressed archive of $SOURCE_DIR -> $TARGET_FILE"
tar -czf "$TARGET_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

echo "[*] Generating SHA-256 checksum verification..."
sha256sum "$TARGET_FILE" > "${TARGET_FILE}.sha256"

echo "[*] Verifying archive integrity..."
tar -tzf "$TARGET_FILE" >/dev/null
echo "[✓] Archive integrity verified."

echo "[*] Pruning archives older than $RETENTION_DAYS days..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +"$RETENTION_DAYS" -delete
find "$BACKUP_DIR" -name "backup_*.sha256" -mtime +"$RETENTION_DAYS" -delete

echo "[✓] Backup complete: $(ls -lh "$TARGET_FILE" | awk '{print $9, "(" $5 ")"}')"
