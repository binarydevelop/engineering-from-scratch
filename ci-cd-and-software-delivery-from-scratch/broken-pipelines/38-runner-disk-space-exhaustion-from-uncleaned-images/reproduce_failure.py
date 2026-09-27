#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 38: 38-runner-disk-space-exhaustion-from-uncleaned-images
Demonstrates: Self-Hosted Runner Fails with 'No space left on device'
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 38-runner-disk-space-exhaustion-from-uncleaned-images")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Build job fails during `docker build` with disk write failure.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
