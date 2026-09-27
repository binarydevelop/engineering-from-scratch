#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 18: 18-dirty-self-hosted-runner-state-leak
Demonstrates: Persistent Self-Hosted Runner Leaves State from Previous Build
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 18-dirty-self-hosted-runner-state-leak")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Build passes on runner A because an uncommitted file was left on disk by a previous run, but fails on runner B.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
