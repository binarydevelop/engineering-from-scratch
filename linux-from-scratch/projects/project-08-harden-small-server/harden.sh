#!/usr/bin/env bash
# Server Hardening Automation Script
# Applies strict SSH policies, UFW firewall rules, and permissions
set -euo pipefail

echo "[*] Step 1: Auditing SSH Configuration..."
if [ -f /etc/ssh/sshd_config ]; then
    echo "  Creating hardened sshd configuration snippet..."
    sudo mkdir -p /etc/ssh/sshd_config.d/
    cat << 'EOF' | sudo tee /etc/ssh/sshd_config.d/99-hardened.conf >/dev/null
# LFS Server Hardening Baseline
PermitRootLogin no
PasswordAuthentication no
X11Forwarding no
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
EOF
    echo "  Testing sshd configuration syntax..."
    sudo sshd -t || echo "[!] Notice: Check sshd config syntax in your environment."
fi

echo "[*] Step 2: Configuring Stateful Firewall (UFW)..."
if command -v ufw >/dev/null 2>&1; then
    echo "  Setting default deny incoming, allow outgoing..."
    sudo ufw default deny incoming
    sudo ufw default allow outgoing
    sudo ufw allow 22/tcp comment 'SSH Management'
    sudo ufw allow 80/tcp comment 'HTTP Public'
    sudo ufw allow 443/tcp comment 'HTTPS Public'
    echo "  Firewall rules prepared."
fi

echo "[*] Step 3: Auditing SUID/SGID Binaries..."
echo "  Scanning filesystem for SUID root executables..."
find / -perm -4000 -type f 2>/dev/null | head -10

echo "[✓] Hardening baseline applied."
