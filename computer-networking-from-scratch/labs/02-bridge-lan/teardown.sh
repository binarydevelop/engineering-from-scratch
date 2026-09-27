#!/usr/bin/env bash
set -euo pipefail
for i in 1 2 3; do sudo ip netns del "ns$i" 2>/dev/null || true; done
sudo ip link del br0 2>/dev/null || true
echo "Lab 02 dismantled."
