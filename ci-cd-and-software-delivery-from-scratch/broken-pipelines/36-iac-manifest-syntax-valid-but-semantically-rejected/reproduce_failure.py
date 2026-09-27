#!/usr/bin/env python3
"""
Reproduction Script for Broken Lab 36: 36-iac-manifest-syntax-valid-but-semantically-rejected
Demonstrates: Kubernetes YAML Valid YAML But Rejected by API Server
"""
import sys
import time

print("========================================================================")
print(" RUNNING BROKEN PIPELINE SIMULATION: 36-iac-manifest-syntax-valid-but-semantically-rejected")
print("========================================================================")
time.sleep(0.05)

# Simulate failure symptoms
print("Executing pipeline stage...", file=sys.stderr)
print("CRITICAL FAILURE DETECTED: CI passes YAML syntax check (`yaml.safe_load`), but deployment fails with `unknown field 'replicas' in Service spec`.", file=sys.stderr)
print("Exit Code: 1 (Stage Failed)", file=sys.stderr)
sys.exit(1)
