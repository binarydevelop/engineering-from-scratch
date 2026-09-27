#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 02: 02-unpinned-floating-dependency-break
Demonstrates: Floating Dependency Range Pulls Breaking Upstream Release
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 02-unpinned-floating-dependency-break")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A pipeline that passed 2 hours ago suddenly fails on clean checkout with ImportError or syntax error, even though zero project code changed.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
