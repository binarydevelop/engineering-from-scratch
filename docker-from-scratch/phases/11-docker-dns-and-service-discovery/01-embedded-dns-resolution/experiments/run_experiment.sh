#!/usr/bin/env bash
# phases/11-docker-dns-and-service-discovery/01-embedded-dns-resolution/experiments/run_experiment.sh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LESSON_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Running Phase 11 Experiment: Docker DNS & Service Discovery ==="

# Cleanup prior test resources
docker rm -f dfs-cache dfs-client dfs-def-1 dfs-def-2 >/dev/null 2>&1 || true
docker network rm dfs-dns-net >/dev/null 2>&1 || true

echo "--- Experiment 1: User-Defined Network (Automatic DNS Enabled) ---"
echo "1. Creating user-defined network 'dfs-dns-net'..."
docker network create dfs-dns-net >/dev/null

echo "2. Launching 'dfs-cache' and 'dfs-client' on dfs-dns-net..."
docker run -d --name dfs-cache --network dfs-dns-net alpine:latest sleep 60 >/dev/null
docker run -d --name dfs-client --network dfs-dns-net alpine:latest sleep 60 >/dev/null

echo ""
echo "3. Inspecting /etc/resolv.conf inside dfs-client:"
docker exec dfs-client cat /etc/resolv.conf

echo ""
echo "4. Resolving 'dfs-cache' by hostname from dfs-client (ping dfs-cache):"
docker exec dfs-client ping -c 2 dfs-cache

echo ""
echo "--- Experiment 2: Default Bridge (DNS Resolution DISABLED) ---"
echo "1. Launching two containers on the default bridge (no --network specified)..."
docker run -d --name dfs-def-1 alpine:latest sleep 60 >/dev/null
docker run -d --name dfs-def-2 alpine:latest sleep 60 >/dev/null

echo "2. Inspecting /etc/resolv.conf on default bridge:"
docker exec dfs-def-1 cat /etc/resolv.conf

echo ""
echo "3. Attempting to resolve 'dfs-def-2' by container name on default bridge (Expect Failure):"
set +e
docker exec dfs-def-1 ping -c 1 dfs-def-2
DEF_PING_EXIT=$?
set -e
if [ "$DEF_PING_EXIT" -ne 0 ]; then
    echo "Observed expected failure: Default bridge has NO embedded DNS resolution!"
fi

echo ""
echo "--- Experiment 3: Dynamic IP Reassignment and DNS Invariance ---"
CACHE_OLD_IP=$(docker inspect dfs-cache --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
echo "Old IP of dfs-cache: $CACHE_OLD_IP"

echo "Recreating dfs-cache..."
docker rm -f dfs-cache >/dev/null
# Launch another dummy container first to consume the old IP
docker run -d --name dfs-dummy --network dfs-dns-net alpine:latest sleep 60 >/dev/null
docker run -d --name dfs-cache --network dfs-dns-net alpine:latest sleep 60 >/dev/null
CACHE_NEW_IP=$(docker inspect dfs-cache --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
echo "New IP of dfs-cache: $CACHE_NEW_IP"

echo "Resolving 'dfs-cache' from dfs-client after IP change:"
docker exec dfs-client ping -c 1 dfs-cache
echo "Confirmed: Service discovery resolved the new IP without reconfiguring client!"

# Cleanup
docker rm -f dfs-cache dfs-client dfs-def-1 dfs-def-2 dfs-dummy >/dev/null
docker network rm dfs-dns-net >/dev/null

echo ""
echo "Phase 11 Experiment Completed Successfully."
