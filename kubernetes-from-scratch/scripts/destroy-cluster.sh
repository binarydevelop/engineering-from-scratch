#!/usr/bin/env bash
set -euo pipefail

# scripts/destroy-cluster.sh
# Destroys the local kind lab cluster cleanly.

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

CLUSTER_NAME="${1:-k8s-scratch-cluster}"

echo "=========================================================="
echo "  Tearing down cluster: $CLUSTER_NAME                     "
echo "=========================================================="

if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    kind delete cluster --name "$CLUSTER_NAME"
    echo "Cluster '$CLUSTER_NAME' has been deleted."
else
    echo "Cluster '$CLUSTER_NAME' does not exist."
fi
