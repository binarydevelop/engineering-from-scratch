#!/usr/bin/env bash
set -euo pipefail

# projects/08-failure-day/scenarios/run_all_drills.sh
# Interactive Chaos Engineering & Failure Day Guide

export PATH="/opt/homebrew/bin:/usr/local/bin:$PATH"

echo "=========================================================="
echo "    kubernetes-from-scratch: Failure Day Drill Suite      "
echo "=========================================================="
echo "This suite demonstrates the 8 canonical failure scenarios."
echo ""

prompt_step() {
    local title="$1"
    local desc="$2"
    echo "----------------------------------------------------------"
    echo ">> $title"
    echo "   $desc"
    echo "----------------------------------------------------------"
    read -p "Press Enter to execute this drill scenario (or Ctrl+C to cancel)..." _
}

# Drill 1: Kill Pod
prompt_step "Drill 01: Kill Pod under ReplicaSet" "Deploying app, deleting a pod, observing ReplicaSet controller replacement."
kubectl create deployment drill-nginx --image=nginx:1.27-alpine --replicas=3
kubectl wait --for=condition=Available deployment/drill-nginx --timeout=60s
POD_TO_KILL=$(kubectl get pods -l app=drill-nginx -o jsonpath='{.items[0].metadata.name}')
echo "Killing pod: $POD_TO_KILL"
kubectl delete pod "$POD_TO_KILL"
echo "Observing ReplicaSet reconciliation:"
kubectl get pods -l app=drill-nginx
kubectl delete deployment drill-nginx

# Drill 2: Broken Image Rollout
prompt_step "Drill 02: Broken Image Rollout" "Deploying v1, updating to non-existent image, inspecting events, rolling back."
kubectl create deployment drill-rollout --image=nginx:1.27-alpine --replicas=3
kubectl wait --for=condition=Available deployment/drill-rollout --timeout=60s
echo "Triggering broken update..."
kubectl set image deployment/drill-rollout nginx=nginx:non-existent-tag-999
sleep 5
kubectl get pods -l app=drill-rollout
echo "Inspecting rollout status:"
kubectl rollout status deployment/drill-rollout --timeout=15s || true
echo "Undoing rollout (reconciling to last known good state):"
kubectl rollout undo deployment/drill-rollout
kubectl rollout status deployment/drill-rollout --timeout=60s
kubectl delete deployment drill-rollout

echo ""
echo "=========================================================="
echo "  Drill completed! Run individual drills in docs/README.md "
echo "=========================================================="
