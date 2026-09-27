#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 34: 34-contract-test-fails-across-service-boundaries
Demonstrates: Service A Drops Field Required by Service B Consumer Contract
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 34-contract-test-fails-across-service-boundaries")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Service A deploys smoothly, but downstream Service B begins failing with JSON deserialization errors.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
