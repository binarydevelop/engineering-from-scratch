#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 41: 41-reusable-workflow-breaking-change-cascades-all-repos
Demonstrates: Unversioned Reusable Workflow Change Breaks 40 Downstream Repos
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 41-reusable-workflow-breaking-change-cascades-all-repos")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Platform team updates shared workflow on `main`; instantly 40 repositories fail their CI runs.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
