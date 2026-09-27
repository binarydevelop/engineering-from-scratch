#!/usr/bin/env bash
set -euo pipefail

# Experiment runner for Phase 108: When Kubernetes Is the Wrong Tool
echo "=========================================================="
echo "  Running Experiment: Phase 108 - When Kubernetes Is the Wrong Tool"
echo "=========================================================="

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

if [ -d "manifests" ] && [ "$(ls -A manifests 2>/dev/null)" ]; then
    echo "Applying manifests..."
    kubectl apply -f manifests/
    echo "Inspecting state:"
    kubectl get all -o wide
fi

echo ""
echo "Experiment completed. Inspect events and record evidence."
