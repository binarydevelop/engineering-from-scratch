#!/usr/bin/env bash
# Automated Deployment Script for LFS Microservice
set -euo pipefail

APP_DIR="/opt/lfs-api"
SERVICE_USER="lfs-service"
CONFIG_DIR="/etc/lfs-api"

echo "[*] Creating dedicated service user: $SERVICE_USER..."
if ! id "$SERVICE_USER" >/dev/null 2>&1; then
    sudo useradd -r -s /usr/sbin/nologin -d "$APP_DIR" "$SERVICE_USER"
fi

echo "[*] Setting up application directories..."
sudo mkdir -p "$APP_DIR" "$CONFIG_DIR" "$APP_DIR/data"

echo "[*] Installing application code and configuration..."
sudo cp server.py "$APP_DIR/server.py"
sudo cp server.env "$CONFIG_DIR/server.env"
sudo chmod 755 "$APP_DIR/server.py"
sudo chmod 640 "$CONFIG_DIR/server.env"
sudo chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"
sudo chown -R "root:$SERVICE_USER" "$CONFIG_DIR"

echo "[*] Installing systemd unit file..."
sudo cp lfs-api.service /etc/systemd/system/lfs-api.service
sudo systemctl daemon-reload
sudo systemctl enable --now lfs-api.service

echo "[*] Verifying service health..."
sleep 2
sudo systemctl status lfs-api.service --no-pager
curl -s http://127.0.0.1:8080/health | jq . || curl -s http://127.0.0.1:8080/health

echo "[✓] Project 01 Deployed Successfully."
