# Lab 03: Systemd Service Sandbox

## Objective
Author, supervise, and debug an unprivileged service unit in an isolated user session or system daemon slot.

## Setup Procedure
```bash
# 1. Create a minimal Python server script
mkdir -p /tmp/lfs-lab/app
cat << 'EOF' > /tmp/lfs-lab/app/server.py
import http.server, os, sys
port = 8085
class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK from LFS Sandboxed Service\n")
print(f"Service running on port {port} (PID: {os.getpid()})")
http.server.HTTPServer(("127.0.0.1", port), Handler).serve_forever()
EOF

# 2. Create systemd user service unit (~/.config/systemd/user/lfs-test.service)
mkdir -p ~/.config/systemd/user
cat << EOF > ~/.config/systemd/user/lfs-test.service
[Unit]
Description=LFS Sandboxed Test Service

[Service]
ExecStart=/usr/bin/python3 /tmp/lfs-lab/app/server.py
Restart=on-failure
RestartSec=3s

[Install]
WantedBy=default.target
EOF

# 3. Reload user daemon & start service
systemctl --user daemon-reload
systemctl --user start lfs-test.service
systemctl --user status lfs-test.service

# 4. Verify reachability
curl http://127.0.0.1:8085
```

## Teardown
```bash
systemctl --user stop lfs-test.service
rm -f ~/.config/systemd/user/lfs-test.service
systemctl --user daemon-reload
rm -rf /tmp/lfs-lab/app
```
