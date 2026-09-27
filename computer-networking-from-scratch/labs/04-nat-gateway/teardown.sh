#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-priv 2>/dev/null || true
sudo ip netns del ns-nat 2>/dev/null || true
sudo ip netns del ns-wan 2>/dev/null || true
echo "Lab 04 dismantled."
