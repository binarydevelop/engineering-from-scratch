#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 19: 19-failing-readiness-probe-causes-deploy-loop
Demonstrates: Readiness Probe Timeout Causes Rolling Deployment Deadlock
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 19-failing-readiness-probe-causes-deploy-loop")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Deployment never completes; Kubernetes restarts new pods continuously and deployment times out after 10 minutes.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
