#!/usr/bin/env python3
"""
inspect_registry_manifest.py
Deconstructs image naming syntax, repo digests, and the OCI Distribution model.
"""

import json
import subprocess
import sys

def parse_image_name(image_ref: str):
    print(f"=== Image Reference Parsing: {image_ref} ===")
    
    # Anatomy: [registry/][namespace/]repository[:tag][@digest]
    digest = ""
    tag = "latest"
    ref = image_ref
    
    if "@" in ref:
        ref, digest = ref.split("@", 1)
    if ":" in ref:
        ref, tag = ref.split(":", 1)
        
    parts = ref.split("/")
    if len(parts) == 1:
        registry = "docker.io (default Docker Hub)"
        namespace = "library (official images)"
        repository = parts[0]
    elif len(parts) == 2:
        if "." in parts[0] or ":" in parts[0] or parts[0] == "localhost":
            registry = parts[0]
            namespace = "root"
            repository = parts[1]
        else:
            registry = "docker.io (default Docker Hub)"
            namespace = parts[0]
            repository = parts[1]
    else:
        registry = parts[0]
        namespace = "/".join(parts[1:-1])
        repository = parts[-1]

    print(f"  Registry Host: {registry}")
    print(f"  Namespace:     {namespace}")
    print(f"  Repository:    {repository}")
    print(f"  Tag:           {tag}")
    print(f"  Digest:        {digest or 'none specified'}")

def inspect_local_digests(image_name: str):
    print(f"\n=== Local RepoDigests for {image_name} ===")
    try:
        raw = subprocess.check_output(["docker", "image", "inspect", image_name]).decode()
        data = json.loads(raw)[0]
        digests = data.get("RepoDigests", [])
        if digests:
            for d in digests:
                print(f"  Immutable Digest: {d}")
        else:
            print("  (Locally built image without remote registry digest)")
    except Exception as e:
        print(f"Error inspecting {image_name}: {e}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "redis:7-alpine"
    parse_image_name(target)
    parse_image_name("ghcr.io/astral-sh/uv:0.4.0")
    parse_image_name("localhost:5000/my-company/auth-service:v2.1@sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855")
    inspect_local_digests(target)
