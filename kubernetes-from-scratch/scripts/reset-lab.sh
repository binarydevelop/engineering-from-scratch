#!/usr/bin/env bash
set -euo pipefail

# scripts/reset-lab.sh
# Resets the cluster workloads, namespaces, and node taints back to baseline
# without needing to recreate the entire cluster.

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "=========================================================="
echo "    kubernetes-from-scratch: Resetting Lab Environment    "
echo "=========================================================="

echo "1. Cleaning non-system namespaces..."
NAMESPACES=$(kubectl get namespaces -o jsonpath='{.items[*].metadata.name}')
for ns in $NAMESPACES; do
    if [[ "$ns" != "default" && "$ns" != "kube-system" && "$ns" != "kube-public" && "$ns" != "kube-node-lease" ]]; then
        echo "   Deleting namespace: $ns"
        kubectl delete namespace "$ns" --timeout=60s || true
    fi
done

echo "2. Cleaning resources in 'default' namespace..."
kubectl delete all --all -n default --timeout=60s || true
kubectl delete pvc --all -n default --timeout=60s || true
kubectl delete configmap --all -n default --timeout=60s || true
kubectl delete secret --all -n default --timeout=60s || true

echo "3. Resetting node taints, labels, and schedulability..."
NODES=$(kubectl get nodes -o jsonpath='{.items[*].metadata.name}')
for node in $NODES; do
    kubectl uncordon "$node" 2>/dev/null || true
    # Remove custom lab labels if present
    kubectl label node "$node" disktype- env- tier- zone- 2>/dev/null || true
    # Remove custom lab taints if present
    kubectl taint nodes "$node" dedicated:NoSchedule- 2>/dev/null || true
    kubectl taint nodes "$node" app=special:NoSchedule- 2>/dev/null || true
done

echo ""
echo "=========================================================="
echo "  Lab reset complete! Current cluster state:              "
echo "=========================================================="
kubectl get nodes
kubectl get all -n default
