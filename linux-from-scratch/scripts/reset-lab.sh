#!/usr/bin/env bash
set -euo pipefail

LAB_DIR="/tmp/lfs-lab"

echo "[*] Resetting linux-from-scratch laboratory environment..."

# 1. Terminate stray lab background processes
pkill -f "lfs-" 2>/dev/null || true

# 2. Clean lab directory
if [ -d "$LAB_DIR" ]; then
    echo "[*] Cleaning directory: $LAB_DIR"
    rm -rf "$LAB_DIR"
fi

mkdir -p "$LAB_DIR"
chmod 755 "$LAB_DIR"

echo "[✓] Laboratory sandbox pristine at: $LAB_DIR"
