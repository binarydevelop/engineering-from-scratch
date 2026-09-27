#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="/tmp/lfs-lab"

echo "[*] Cleaning up temporary laboratory artifacts..."

# 1. Unmount any temporary loopback filesystems safely
if [ -d "$LAB_DIR/mnt" ]; then
    if mountpoint -q "$LAB_DIR/mnt"; then
        echo "[*] Unmounting $LAB_DIR/mnt..."
        sudo umount "$LAB_DIR/mnt" || true
    fi
fi

# 2. Detach loop devices associated with /tmp/
for loop in $(losetup -j "$LAB_DIR" 2>/dev/null | cut -d: -f1 || true); do
    echo "[*] Detaching loop device: $loop"
    sudo losetup -d "$loop" || true
done

# 3. Clean files
rm -rf "$LAB_DIR"
rm -f /tmp/lfs-*.img /tmp/lfs-*.log /tmp/lfs-*.pid /tmp/lfs-*.sock

echo "[✓] Cleanup complete."
