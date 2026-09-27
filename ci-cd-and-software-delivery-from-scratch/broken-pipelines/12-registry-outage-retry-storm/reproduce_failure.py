#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 12: 12-registry-outage-retry-storm
Demonstrates: Container Registry Throttling Causes Pipeline Retry Storm
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 12-registry-outage-retry-storm")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Pipelines all fail with `HTTP 429 Too Many Requests` or `HTTP 503 Service Unavailable` during image pull.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
