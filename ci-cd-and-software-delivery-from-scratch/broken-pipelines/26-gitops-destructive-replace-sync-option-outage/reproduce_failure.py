#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 26: 26-gitops-destructive-replace-sync-option-outage
Demonstrates: Argo CD Replace Sync Option Deletes Running Resources
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 26-gitops-destructive-replace-sync-option-outage")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: Enabling `--replace` in sync options deletes active Deployment pods, causing an outage instead of a rolling update.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
