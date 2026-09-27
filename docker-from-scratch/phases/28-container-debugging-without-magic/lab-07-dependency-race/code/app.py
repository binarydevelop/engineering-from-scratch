import socket
import sys
import time

host = "db"
port = 5432

print(f"[*] App starting... attempting immediate TCP connection to {host}:{port}...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(2.0)

try:
    s.connect((host, port))
    s.close()
    print(f"[+] SUCCESS: Connected to {host}:{port}! Service is ready.")
    sys.exit(0)
except Exception as e:
    print(f"[-] ERROR: Connection failed: {e}", file=sys.stderr)
    print("[-] First Principles Diagnostic: 'depends_on' only waits for container creation, not TCP readiness.", file=sys.stderr)
    sys.exit(1)
