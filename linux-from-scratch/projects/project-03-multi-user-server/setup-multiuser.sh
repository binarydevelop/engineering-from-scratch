#!/usr/bin/env bash
# Multi-User Collaboration Directory Setup
set -euo pipefail

SHARED_DIR="/tmp/lfs-lab/projects/core"
SHARED_GROUP="lfs-devs"

echo "[*] Setting up collaboration group: $SHARED_GROUP..."
if ! getent group "$SHARED_GROUP" >/dev/null 2>&1; then
    sudo groupadd "$SHARED_GROUP"
fi

echo "[*] Adding current user ($USER) to $SHARED_GROUP..."
sudo usermod -aG "$SHARED_GROUP" "$USER"

echo "[*] Creating shared project directory: $SHARED_DIR..."
sudo mkdir -p "$SHARED_DIR"

echo "[*] Enforcing SGID bit and group ownership..."
sudo chgrp "$SHARED_GROUP" "$SHARED_DIR"
sudo chmod 2770 "$SHARED_DIR"

echo "[*] Enforcing default POSIX ACLs for group write..."
if command -v setfacl >/dev/null 2>&1; then
    sudo setfacl -d -m g::rwx "$SHARED_DIR"
    sudo setfacl -d -m o::--- "$SHARED_DIR"
fi

echo "[✓] Directory configured: $(ls -ld "$SHARED_DIR")"
