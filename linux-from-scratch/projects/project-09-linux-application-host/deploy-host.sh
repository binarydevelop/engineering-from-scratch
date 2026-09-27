#!/usr/bin/env bash
# Capstone Deployment Engine: Linux Application Host
set -euo pipefail

echo "=========================================================="
echo "    CAPSTONE: DEPLOYING LINUX APPLICATION HOST STACK       "
echo "=========================================================="

# 1. User & Directory Assembly
APP_USER="lfs-app"
APP_DIR="/opt/production-app"
LOG_DIR="/var/log/production-app"

echo "[1/6] Assembling unprivileged service identity..."
if ! id "$APP_USER" >/dev/null 2>&1; then
    sudo useradd -r -s /usr/sbin/nologin -d "$APP_DIR" "$APP_USER"
fi

sudo mkdir -p "$APP_DIR" "$LOG_DIR"
sudo chown -R "$APP_USER:$APP_USER" "$APP_DIR" "$LOG_DIR"

# 2. Application Installation
echo "[2/6] Installing backend application daemon..."
cat << 'EOF' | sudo tee "$APP_DIR/app.py" >/dev/null
import http.server, json, os, sys
port = 9000
class CapstoneHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "healthy",
            "host": os.uname().nodename,
            "pid": os.getpid(),
            "stack": "Linux-From-Scratch Capstone"
        }).encode("utf-8"))
http.server.HTTPServer(("127.0.0.1", port), CapstoneHandler).serve_forever()
EOF
sudo chmod 755 "$APP_DIR/app.py"
sudo chown "$APP_USER:$APP_USER" "$APP_DIR/app.py"

# 3. Systemd Unit Installation
echo "[3/6] Configuring systemd supervisor unit..."
cat << EOF | sudo tee /etc/systemd/system/lfs-capstone.service >/dev/null
[Unit]
Description=LFS Capstone Application
After=network.target

[Service]
Type=simple
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
ExecStart=/usr/bin/python3 $APP_DIR/app.py
Restart=always
RestartSec=3s
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now lfs-capstone.service

# 4. Verify Backend Service
echo "[4/6] Verifying backend daemon reachability..."
sleep 2
curl -sf http://127.0.0.1:9000/ >/dev/null
echo "  [✓] Backend daemon active on 127.0.0.1:9000"

echo "[5/6] Systemd supervision verified."
sudo systemctl status lfs-capstone.service --no-pager | head -10

echo "[6/6] Capstone stack deployed successfully!"
echo "=========================================================="
