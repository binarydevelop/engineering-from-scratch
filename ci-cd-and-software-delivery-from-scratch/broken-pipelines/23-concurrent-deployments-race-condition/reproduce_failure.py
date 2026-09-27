#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 23: 23-concurrent-deployments-race-condition
Demonstrates: Two Workflows Racing to Deploy Different Commits to Production
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 23-concurrent-deployments-race-condition")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Commit A finishes deploying after Commit B, overwriting newer code with older code.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
