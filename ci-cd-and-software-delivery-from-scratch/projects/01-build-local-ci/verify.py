#!/usr/bin/env python3
import os
import subprocess
import sys

print("Verifying Project 01: Local CI Runner...")
runner_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../pipelines/local_runner.py"))
p = subprocess.run([sys.executable, runner_script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

if p.returncode == 0 and "PIPELINE SUMMARY" in p.stdout:
    print("✓ Project 01 verification PASSED! Local CI engine successfully executed pipeline DAG.")
    sys.exit(0)
else:
    print("✗ Project 01 verification FAILED!", file=sys.stderr)
    print(p.stderr, file=sys.stderr)
    sys.exit(1)
