#!/usr/bin/env bash
set -euo pipefail

# scripts/cluster-status.sh
# Inspects control plane, worker nodes, and core control plane pods.

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "=========================================================="
echo "    kubernetes-from-scratch: Cluster Health & Status      "
echo "=========================================================="

echo ""
echo "1. Cluster Info & API Endpoint:"
kubectl cluster-info

echo ""
echo "2. Node Topology & Container Runtime:"
kubectl get nodes -o wide

echo ""
echo "3. Control Plane System Pods (kube-system):"
kubectl get pods -n kube-system -o wide

echo ""
echo "4. Namespaces & Custom Workloads:"
kubectl get namespaces

echo ""
echo "5. Core DNS & Virtual IP Endpoints:"
kubectl get svc -n kube-system kube-dns -o wide || true
