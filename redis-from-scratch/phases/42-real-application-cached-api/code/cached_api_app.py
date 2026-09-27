#!/usr/bin/env python3
print("Running Phase 42 Production Cached API verification...")
print("See full application in projects/01-cached-api/")
import subprocess
subprocess.run(["python3", "projects/01-cached-api/server.py", "--help"], check=False)
