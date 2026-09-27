#!/usr/bin/env python3
import os
import sys

TARGET = "/data/audit.log"
print(f"[WRITER] Running as UID: {os.getuid()}, GID: {os.getgid()}")
print(f"[WRITER] Attempting write to {TARGET}...")

try:
    with open(TARGET, "a") as f:
        f.write(f"Audit log entry written by UID {os.getuid()}\n")
    print(f"--> [SUCCESS] Successfully wrote to {TARGET}!")
except PermissionError as e:
    print(f"--> [FATAL PERMISSION ERROR] {e}", file=sys.stderr)
    sys.exit(13)
