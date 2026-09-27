#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 20: 20-deploy-succeeds-but-app-crashes-on-startup
Demonstrates: Missing Environment Variable Causes Instant Crash on First Request
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 20-deploy-succeeds-but-app-crashes-on-startup")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Kubernetes rollout finishes successfully (`exit 0`), but all incoming customer requests fail with HTTP 500.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
