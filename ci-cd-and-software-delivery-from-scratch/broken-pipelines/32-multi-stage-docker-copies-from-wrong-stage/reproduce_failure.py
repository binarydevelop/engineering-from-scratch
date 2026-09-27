#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 32: 32-multi-stage-docker-copies-from-wrong-stage
Demonstrates: Multi-Stage Build Copies Host Source Instead of Compiled Binary
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 32-multi-stage-docker-copies-from-wrong-stage")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Container image starts up but fails with `source code not compiled` or huge image size.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
