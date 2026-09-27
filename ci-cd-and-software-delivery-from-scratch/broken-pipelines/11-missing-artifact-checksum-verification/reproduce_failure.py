#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 11: 11-missing-artifact-checksum-verification
Demonstrates: Corrupted or Tampered Artifact Deployed Without Hash Check
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 11-missing-artifact-checksum-verification")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Deployment begins rolling out a truncated tarball or incomplete image, causing pods to enter CrashLoopBackOff.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
