#!/usr/bin/env python3
"""
inspect_container_lifecycle.py
Inspects an existing or exited container's state, entrypoint, and exit code
directly from Docker Engine inspection metadata.
"""

import json
import subprocess
import sys

def inspect_container(container_id: str):
    try:
        raw_json = subprocess.check_output(["docker", "inspect", container_id]).decode()
        data = json.loads(raw_json)[0]
    except Exception as e:
        print(f"Failed to inspect container '{container_id}': {e}", file=sys.stderr)
        sys.exit(1)

    state = data.get("State", {})
    config = data.get("Config", {})
    
    print(f"=== Container Lifecycle State: {container_id} ===")
    print(f"Image ID:      {data.get('Image')}")
    print(f"Created At:    {data.get('Created')}")
    print(f"Status:        {state.get('Status')}")
    print(f"Running:       {state.get('Running')}")
    print(f"Exit Code:     {state.get('ExitCode')}")
    print(f"Started At:    {state.get('StartedAt')}")
    print(f"Finished At:   {state.get('FinishedAt')}")
    print(f"OOMKilled:     {state.get('OOMKilled')}")
    print(f"Path/Cmd:      {data.get('Path')} {' '.join(data.get('Args', []))}")
    print(f"Entrypoint:    {config.get('Entrypoint')}")
    print(f"Env:           {config.get('Env')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_container_lifecycle.py <CONTAINER_ID_OR_NAME>")
        sys.exit(1)
    inspect_container(sys.argv[1])
