#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 39: 39-dora-metric-manipulation-fake-deployments
Demonstrates: Automated Rebuilds Inflat DORA Deployment Frequency
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 39-dora-metric-manipulation-fake-deployments")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: DORA dashboard shows 50 deployments/day, but only 1 real feature shipped; metrics are meaningless.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
