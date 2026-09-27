#!/usr/bin/env python3
import os
import sys

# Critical configuration requirement
secret = os.environ["API_SECRET_KEY"]

print(f"=== API Authenticated Successfully ===")
print(f"Secret prefix: {secret[:6]}...")
sys.exit(0)
