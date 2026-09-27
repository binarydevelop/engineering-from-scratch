#!/usr/bin/env python3
"""
Verification Suite for Capstone 2: Continuous Delivery & Environment Promotion
"""
import os
import subprocess
import sys

print("Verifying Capstone 2: Continuous Delivery & Environment Promotion...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = """bash scripts/release.sh 2.0.0"""
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Capstone verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Capstone verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
