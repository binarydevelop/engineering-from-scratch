#!/usr/bin/env bash
set -euo pipefail
sudo ip netns del ns-alpha 2>/dev/null || true
sudo ip netns del ns-beta 2>/dev/null || true
echo "Lab 01 dismantled."
