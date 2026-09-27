#!/usr/bin/env python3
"""
inspect_image_layers.py
Deconstructs a local Docker image into its constituent layers,
content-addressable hashes, architecture metadata, and execution config.
"""

import json
import subprocess
import sys

def inspect_image(image_name: str):
    try:
        raw = subprocess.check_output(["docker", "image", "inspect", image_name]).decode()
        data = json.loads(raw)[0]
    except Exception as e:
        print(f"Error inspecting image '{image_name}': {e}", file=sys.stderr)
        sys.exit(1)

    print(f"=== Image Deconstruction: {image_name} ===")
    print(f"Image ID:      {data.get('Id')}")
    print(f"RepoTags:      {data.get('RepoTags')}")
    print(f"Architecture:  {data.get('Architecture')} ({data.get('Os')})")
    print(f"Size on Disk:  {data.get('Size', 0) / (1024 * 1024):.2f} MB")
    
    config = data.get("Config", {})
    print("\n--- Default Execution Config ---")
    print(f"Cmd:         {config.get('Cmd')}")
    print(f"Entrypoint:  {config.get('Entrypoint')}")
    print(f"WorkingDir:  {config.get('WorkingDir') or '/'}")
    print(f"Env:         {config.get('Env')}")

    rootfs = data.get("RootFS", {})
    layers = rootfs.get("Layers", [])
    print(f"\n--- RootFS Layers ({len(layers)} layer{'s' if len(layers) != 1 else ''}) ---")
    for idx, layer_hash in enumerate(layers):
        print(f"  Layer {idx + 1}: {layer_hash}")

    print("\n--- Image History (Build Steps) ---")
    try:
        history = subprocess.check_output(["docker", "history", "--no-trunc", image_name]).decode()
        for line in history.splitlines()[:5]:
            print(f"  {line[:100]}...")
    except Exception:
        pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 inspect_image_layers.py <IMAGE_NAME_OR_ID>")
        sys.exit(1)
    inspect_image(sys.argv[1])
