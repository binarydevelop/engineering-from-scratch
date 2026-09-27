#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-mtu-client 2>/dev/null || true
sudo ip netns del ns-mtu-server 2>/dev/null || true
echo "Lab 06 dismantled."
