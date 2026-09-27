#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-firewall 2>/dev/null || true
echo "Lab 05 dismantled."
