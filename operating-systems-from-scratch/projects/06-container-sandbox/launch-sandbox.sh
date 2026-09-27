#!/usr/bin/env bash
# launch-sandbox.sh: Demonstrates container isolation using Linux unshare and cgroups v2
set -euo pipefail

echo "================================================================"
echo "Capstone 6: Linux Container Sandbox Launcher"
echo "================================================================"

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "[!] Notice: Linux namespaces and cgroups require a Linux kernel."
    echo "[!] On macOS or Windows, run this script inside Docker or a Lima VM:"
    echo "    docker run --rm -it --privileged -v \"\$(pwd)\":/lab -w /lab ubuntu:24.04 bash"
    exit 0
fi

if [[ $EUID -ne 0 ]]; then
    echo "[!] Error: Root privileges (or CAP_SYS_ADMIN) required for unshare and cgroup creation."
    echo "    Please run with: sudo ./launch-sandbox.sh"
    exit 1
fi

CGROUP_DIR="/sys/fs/cgroup/tiny-container"
mkdir -p "${CGROUP_DIR}"

# Set 100MB memory limit using cgroups v2
if [[ -f "${CGROUP_DIR}/memory.max" ]]; then
    echo "104857600" > "${CGROUP_DIR}/memory.max"
    echo "[x] Configured cgroup v2 memory limit: 100 MB"
fi

echo "[x] Spawning isolated namespace container..."
unshare --pid --uts --mount --net --fork bash -c "
    echo '[Container] Active PID:' \$\$
    hostname tiny-container-node
    echo '[Container] Hostname:' \$(hostname)
    echo '[Container] Exiting container sandbox.'
"

# Cleanup cgroup
rmdir "${CGROUP_DIR}" 2>/dev/null || true
echo "[x] Cleanup complete."
