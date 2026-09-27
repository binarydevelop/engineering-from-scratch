#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 25: 25-gitops-reconciler-deploys-bad-desired-state
Demonstrates: GitOps Controller Faithfully Deploys Broken Config Commit
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 25-gitops-reconciler-deploys-bad-desired-state")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: An invalid YAML syntax or broken image tag was merged into main; Argo CD syncs it immediately, taking down production.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
