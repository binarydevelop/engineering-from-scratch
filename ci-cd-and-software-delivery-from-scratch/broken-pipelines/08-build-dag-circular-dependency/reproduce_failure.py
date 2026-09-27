#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 08: 08-build-dag-circular-dependency
Demonstrates: Circular Dependency in Build Graph Halts Pipeline
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 08-build-dag-circular-dependency")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Build tool hangs indefinitely or crashes with `RecursionError: cyclic dependency detected between target A and target B`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
