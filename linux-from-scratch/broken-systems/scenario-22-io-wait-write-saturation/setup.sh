#!/usr/bin/env bash
# Reproduction script for System Sluggish with High %wa in Top
set -euo pipefail

LAB_DIR="/tmp/lfs-lab/scenario-22-io-wait-write-saturation"
mkdir -p "$LAB_DIR"

echo "[*] Setting up failure environment for System Sluggish with High %wa in Top..."
# Create safe isolated lab markers
echo "FAIL" > "$LAB_DIR/status"

# Isolated reproduction
if [ "scenario-22-io-wait-write-saturation" = "scenario-01-web-server-port-conflict" ]; then
    python3 -c "import socket, time; s = socket.socket(); s.bind(('127.0.0.1', 8080)); s.listen(1); time.sleep(300)" &
    echo $! > "$LAB_DIR/rogue.pid"
    echo "[!] Rogue process listening on 127.0.0.1:8080 (PID: $(cat "$LAB_DIR/rogue.pid"))"
elif [ "scenario-22-io-wait-write-saturation" = "scenario-04-directory-permission-traversal" ]; then
    mkdir -p "$LAB_DIR/data/apps"
    echo "SECRET_KEY=production_token" > "$LAB_DIR/data/apps/settings.env"
    chmod 644 "$LAB_DIR/data/apps/settings.env"
    chmod 644 "$LAB_DIR/data/apps" # Missing +x execute traversal!
elif [ "scenario-22-io-wait-write-saturation" = "scenario-10-path-hijack-or-order" ]; then
    mkdir -p "$LAB_DIR/bin"
    cat << 'EOF' > "$LAB_DIR/bin/uptime"
#!/usr/bin/env bash
echo "ERROR: License key required to run uptime." >&2
exit 1
EOF
    chmod +x "$LAB_DIR/bin/uptime"
fi

echo "[✓] Environment broken. Inspect system and run verify.sh when resolved."
