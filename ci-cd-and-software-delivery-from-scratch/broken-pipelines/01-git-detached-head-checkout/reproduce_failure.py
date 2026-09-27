#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 01: 01-git-detached-head-checkout
Demonstrates: Detached HEAD Commit Never Pushed or Tracked
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 01-git-detached-head-checkout")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: CI checks out a commit in detached HEAD mode. A subsequent git push or branch tag step fails silently or errors with 'fatal: You are not currently on a branch'.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
