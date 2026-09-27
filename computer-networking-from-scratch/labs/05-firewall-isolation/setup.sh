#!/usr/bin/env bash
set -euo pipefail
sudo ip netns add ns-firewall
sudo ip netns exec ns-firewall ip link set lo up
echo "Lab 05 active inside ns-firewall."
