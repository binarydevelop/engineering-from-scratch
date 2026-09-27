#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 22: 22-rollback-fails-due-to-irreversible-migration
Demonstrates: Application Rollback Fails Because Schema Cannot Be Reverted
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 22-rollback-fails-due-to-irreversible-migration")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: New v2 application had a bug. On-call engineer redeploys v1 container image, but v1 crashes on startup because schema changed.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
