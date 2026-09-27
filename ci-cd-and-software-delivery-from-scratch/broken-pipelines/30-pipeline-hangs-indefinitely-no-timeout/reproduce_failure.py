#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 30: 30-pipeline-hangs-indefinitely-no-timeout
Demonstrates: Interactive Prompt Hangs CI Runner For 6 Hours
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 30-pipeline-hangs-indefinitely-no-timeout")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: A command (e.g. `npm init` or `apt-get install` without `-y`) prompts `Are you sure? [y/N]` and hangs until runner timeout.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
