#!/usr/bin/env bash
set -euo pipefail

echo "=========================================================="
echo "    linux-from-scratch : Environment Diagnostics Check    "
echo "=========================================================="

# 1. Operating System & Distribution
if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    . /etc/os-release
    echo "[OK] Distribution : $NAME $VERSION"
else
    echo "[WARN] /etc/os-release not found. (Non-standard Linux or container?)"
fi

# 2. Kernel Details
KERNEL_RELEASE=$(uname -r)
KERNEL_ARCH=$(uname -m)
echo "[OK] Kernel       : $KERNEL_RELEASE ($KERNEL_ARCH)"

# 3. Shell
echo "[OK] Shell        : $BASH_VERSION"

# 4. Privilege check
if [ "$(id -u)" -eq 0 ]; then
    echo "[INFO] Running as root (UID 0)"
else
    echo "[OK] Running as standard user: $(whoami) (UID: $(id -u))"
    if sudo -n true 2>/dev/null; then
        echo "[OK] Passwordless sudo available for root labs"
    else
        echo "[INFO] sudo requires password or not configured"
    fi
fi

# 5. Core Utilities Audit
echo "--- Checking Diagnostic Utilities ---"
REQUIRED_TOOLS=(
    "ps" "top" "free" "vmstat"
    "ip" "ss"
    "ls" "cp" "stat" "cat" "grep" "sed" "awk" "find" "xargs"
    "lsblk" "mount" "umount"
    "curl" "strace" "lsof"
)

MISSING=0
for tool in "${REQUIRED_TOOLS[@]}"; do
    if command -v "$tool" >/dev/null 2>&1; then
        echo "  [✓] $tool"
    else
        echo "  [✗] MISSING: $tool"
        MISSING=$((MISSING + 1))
    fi
done

# 6. systemd Detection
if pidof systemd >/dev/null 2>&1; then
    echo "[OK] init system  : systemd is PID 1"
else
    echo "[WARN] init system: PID 1 is NOT systemd. (Container or WSL1 environment)"
fi

echo "=========================================================="
if [ "$MISSING" -eq 0 ]; then
    echo "Status: ALL CORE TOOLS DETECTED. Environment ready for curriculum."
else
    echo "Status: $MISSING tools missing. Install missing packages with: sudo apt install coreutils iproute2 procps util-linux lsof strace curl"
fi
echo "=========================================================="
