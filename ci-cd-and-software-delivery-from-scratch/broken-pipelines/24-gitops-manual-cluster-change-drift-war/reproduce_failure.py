#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 24: 24-gitops-manual-cluster-change-drift-war
Demonstrates: Manual 'kubectl edit' Reverted in Endless Fight With Reconciler
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 24-gitops-manual-cluster-change-drift-war")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Engineer scales replicas to 10 for emergency traffic; Argo CD continuously resets replicas back to 3 every 3 minutes.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
