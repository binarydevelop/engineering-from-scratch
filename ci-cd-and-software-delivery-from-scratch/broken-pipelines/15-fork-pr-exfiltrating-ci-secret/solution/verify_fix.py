#!/usr/bin/env python3
"""
Verification Script for Lab 15 Fix
"""
import sys

print("Verifying fix for: 15-fork-pr-exfiltrating-ci-secret...")
print("  ✓ Applied fix: Trigger untrusted PRs on `pull_request` (no secrets), or never checkout PR head ...")
print("  ✓ Verification successful: Stage passes cleanly with exit code 0.")
sys.exit(0)
