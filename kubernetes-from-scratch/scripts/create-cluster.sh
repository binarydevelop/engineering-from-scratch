#!/usr/bin/env bash
set -euo pipefail

# scripts/create-cluster.sh
# Provisions a reproducible multi-node kind cluster pinned to Kubernetes v1.37.0.

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

CLUSTER_NAME="${1:-k8s-scratch-cluster}"
NODE_IMAGE="kindest/node:v1.37.0"

echo "=========================================================="
echo "  Creating Cluster: $CLUSTER_NAME (Kubernetes v1.37.0)    "
echo "=========================================================="

if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "Cluster '$CLUSTER_NAME' already exists."
    echo "Switching kubectl context to kind-$CLUSTER_NAME..."
    kubectl config use-context "kind-$CLUSTER_NAME"
    exit 0
fi

KIND_CONFIG=$(mktemp)
cat <<EOF > "$KIND_CONFIG"
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: ${CLUSTER_NAME}
nodes:
- role: control-plane
  image: ${NODE_IMAGE}
  extraPortMappings:
  - containerPort: 80
    hostPort: 8080
    listenAddress: "127.0.0.1"
    protocol: TCP
  - containerPort: 443
    hostPort: 8443
    listenAddress: "127.0.0.1"
    protocol: TCP
- role: worker
  image: ${NODE_IMAGE}
- role: worker
  image: ${NODE_IMAGE}
EOF

echo "Provisioning 1 control-plane and 2 worker nodes..."
kind create cluster --name "$CLUSTER_NAME" --config "$KIND_CONFIG" --wait 3m

rm -f "$KIND_CONFIG"

echo ""
echo "Setting kubectl context..."
kubectl config use-context "kind-$CLUSTER_NAME"

echo ""
echo "Waiting for all nodes to report Ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

echo ""
echo "=========================================================="
echo "  Cluster is Ready! Multi-node topology online:           "
echo "=========================================================="
kubectl get nodes -o wide
