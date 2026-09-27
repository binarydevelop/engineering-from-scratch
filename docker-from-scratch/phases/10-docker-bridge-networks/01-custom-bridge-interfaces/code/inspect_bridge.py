#!/usr/bin/env python3
"""
inspect_bridge.py
Inspects a Docker bridge network: extracts Subnet, Gateway, Driver,
and active attached container endpoints with their allocated IP addresses.
"""

import json
import subprocess
import sys

def inspect_network(network_name: str):
    try:
        raw = subprocess.check_output(["docker", "network", "inspect", network_name]).decode()
        data = json.loads(raw)[0]
    except Exception as e:
        print(f"Error inspecting network '{network_name}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"=== Docker Network Inspection: {network_name} ===")
    print(f"Network ID:   {data.get('Id')[:12]}")
    print(f"Driver:       {data.get('Driver')}")
    print(f"Scope:        {data.get('Scope')}")
    print(f"Internal:     {data.get('Internal')}")

    ipam_configs = data.get("IPAM", {}).get("Config", [])
    print("\n--- IP Address Management (IPAM) ---")
    for cfg in ipam_configs:
        print(f"  Subnet:  {cfg.get('Subnet')}")
        print(f"  Gateway: {cfg.get('Gateway')}")

    containers = data.get("Containers", {})
    print(f"\n--- Attached Container Endpoints ({len(containers)}) ---")
    if not containers:
        print("  (No containers currently connected)")
    for cid, cdata in containers.items():
        print(f"  Container: {cdata.get('Name')}")
        print(f"    IPv4: {cdata.get('IPv4Address')}")
        print(f"    MAC:  {cdata.get('MacAddress')}")

if __name__ == "__main__":
    net = sys.argv[1] if len(sys.argv) > 1 else "bridge"
    inspect_network(net)
