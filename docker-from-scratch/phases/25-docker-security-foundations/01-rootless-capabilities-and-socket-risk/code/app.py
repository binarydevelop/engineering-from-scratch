#!/usr/bin/env python3
"""
app.py
Security audit helper: inspects process credentials (UID/GID)
and attempts restricted actions to verify least privilege enforcement.
"""

import os
import sys

def audit():
    uid = os.getuid()
    gid = os.getgid()
    print(f"=== Process Security Context ===")
    print(f"Current UID: {uid} ({'root' if uid == 0 else 'non-root unprivileged'})")
    print(f"Current GID: {gid}")
    
    # Try writing to a protected system directory
    test_target = "/etc/malicious_config.conf"
    try:
        with open(test_target, "w") as f:
            f.write("injected payload\n")
        print(f"[SECURITY VULNERABILITY] Successfully wrote to protected system path {test_target}!")
    except PermissionError:
        print(f"[SECURITY VERIFIED] Write to {test_target} rejected with PermissionError (Least privilege enforced).")

if __name__ == "__main__":
    audit()
