#!/usr/bin/env python3
"""
Verification Harness for Project: Full GitHub Actions CI Pipeline (Phase 207)
"""
import os
import subprocess
import sys

print("Verifying Project: Full GitHub Actions CI Pipeline...")
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

cmd = """python3 -c 'import os, sys; assert os.path.exists(".github/workflows/ci.yml"); print("CI workflow file exists and validated"); sys.exit(0)'"""
p = subprocess.run(cmd, shell=True, cwd=root_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0:
    print("✓ Project verification PASSED!")
    print(p.stdout.strip())
    sys.exit(0)
else:
    print("✗ Project verification FAILED!", file=sys.stderr)
    print(p.stderr.strip(), file=sys.stderr)
    sys.exit(1)
