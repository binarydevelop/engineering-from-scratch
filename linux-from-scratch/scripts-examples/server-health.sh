#!/usr/bin/env bash
# Production Server Health Audit Tool
# Reads directly from Linux virtual filesystems (/proc) and core diagnostic utilities
set -euo pipefail

echo "================================================================="
echo "                 PRODUCTION LINUX HEALTH REPORT                  "
echo "================================================================="
echo "Report Generated: $(date -u '+%Y-%m-%d %H:%M:%S UTC')"
echo "Host            : $(hostname -f 2>/dev/null || hostname)"
echo "Kernel          : $(uname -r) ($(uname -m))"
echo "Uptime          : $(uptime -p 2>/dev/null || uptime)"

echo ""
echo "--- [1] LOAD AVERAGE & CPU UTILIZATION ---"
echo "Load Averages (1, 5, 15 min): $(awk '{print $1, $2, $3}' /proc/loadavg)"
CPU_CORES=$(grep -c ^processor /proc/cpuinfo)
echo "Total CPU Cores             : $CPU_CORES"

echo ""
echo "--- [2] MEMORY CONSUMPTION (/proc/meminfo) ---"
awk '
/^MemTotal:/     {total=$2/1024}
/^MemFree:/      {free=$2/1024}
/^MemAvailable:/ {avail=$2/1024}
/^SwapTotal:/    {swapt=$2/1024}
/^SwapFree:/     {swapf=$2/1024}
END {
    printf "Total RAM     : %8.2f MB\n", total
    printf "Available RAM : %8.2f MB (%.1f%%)\n", avail, (avail/total)*100
    printf "Free RAM      : %8.2f MB\n", free
    if (swapt > 0) {
        printf "Swap Used     : %8.2f MB / %.2f MB\n", (swapt-swapf), swapt
    } else {
        printf "Swap          : Disabled / None\n"
    }
}' /proc/meminfo

echo ""
echo "--- [3] ROOT & LOCAL FILESYSTEM USAGE ---"
df -hT --exclude-type=tmpfs --exclude-type=devtmpfs

echo ""
echo "--- [4] LISTENING NETWORK SERVICES ---"
if command -v ss >/dev/null 2>&1; then
    ss -lntp 2>/dev/null | head -15 || echo "Requires root to view all owning process names."
fi

echo ""
echo "--- [5] SYSTEMD FAILED UNITS ---"
if command -v systemctl >/dev/null 2>&1; then
    FAILED=$(systemctl --failed --no-legend 2>/dev/null || true)
    if [ -z "$FAILED" ]; then
        echo "All systemd units healthy (0 failed)."
    else
        echo "ALERT: The following systemd units have failed:"
        echo "$FAILED"
    fi
fi
echo "================================================================="
