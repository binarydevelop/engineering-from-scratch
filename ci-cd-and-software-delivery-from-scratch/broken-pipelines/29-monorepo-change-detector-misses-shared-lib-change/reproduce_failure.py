#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 29: 29-monorepo-change-detector-misses-shared-lib-change
Demonstrates: Monorepo Pipeline Skips Testing Downstream Dependent Service
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 29-monorepo-change-detector-misses-shared-lib-change")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A change to `libs/auth` is merged; Service B CI passes because it didn't test Service B, which broke in production.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
