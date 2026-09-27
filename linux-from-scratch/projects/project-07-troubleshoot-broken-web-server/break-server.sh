#!/usr/bin/env bash
# Multi-Fault Setup for Project 07: Troubleshoot a Broken Web Server
set -euo pipefail

LAB_DIR="/tmp/lfs-lab/project-07"
mkdir -p "$LAB_DIR"

echo "[*] Injecting Fault 1: Blocking backend port 8080 with dummy listener..."
python3 -c "import socket, time; s=socket.socket(); s.bind(('127.0.0.1', 8080)); s.listen(1); time.sleep(600)" &
echo $! > "$LAB_DIR/rogue_port.pid"

echo "[*] Injecting Fault 2: Creating broken unix domain socket with no permissions..."
touch "$LAB_DIR/app.sock"
chmod 000 "$LAB_DIR/app.sock"

echo "[*] Injecting Fault 3: Simulating disk quota saturation with sparse dummy file..."
truncate -s 50M "$LAB_DIR/ghost.bin"

echo "[!] System broken with multiple interacting faults."
echo "Follow the 10-step triage sequence to isolate and remediate all faults."
