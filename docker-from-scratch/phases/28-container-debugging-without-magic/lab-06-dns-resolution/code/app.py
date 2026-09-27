import socket
import sys
import time

target = sys.argv[1] if len(sys.argv) > 1 else "cache"

print(f"[*] Attempting to resolve hostname: {target}...")
try:
    ip = socket.gethostbyname(target)
    print(f"[+] SUCCESS: Resolved '{target}' to IP {ip}")
    sys.exit(0)
except socket.gaierror as e:
    print(f"[-] ERROR: Failed to resolve '{target}': {e}", file=sys.stderr)
    print("[-] First Principles Diagnostic: Embedded DNS (127.0.0.11) is inactive on the default bridge.", file=sys.stderr)
    sys.exit(1)
