#!/usr/bin/env python3
"""
trace_full_stack.py
Deconstructs a running Docker container / Compose service across all 14 layers
from the terminal invocation down to kernel data structures.
"""

import os
import sys
import json
import subprocess
import socket

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"ERROR: {e.stderr.strip()}"

def main():
    print("=" * 80)
    print("PHASE 30: THE FINAL MENTAL MODEL - END-TO-END EXECUTION TRACE")
    print("=" * 80)

    # 1. Terminal & CLI
    print("\n[Layer 1: Terminal & CLI]")
    print("  Command: 'docker compose up -d' or 'docker run'")
    print("  Role: CLI parses flags, loads environment (.env), builds compose DAG model.")

    # 2. Docker Engine API
    print("\n[Layer 2: Docker Engine REST API]")
    sock_path = "/var/run/docker.sock"
    if os.path.exists(sock_path):
        print(f"  Unix Socket: {sock_path} exists and is accessible.")
        print("  Protocol: HTTP/1.1 over AF_UNIX sockets (`POST /v1.45/containers/create`).")
    else:
        print(f"  Unix Socket: {sock_path} not found directly on host filesystem.")

    # 3. Image Layers & Content-Addressable Storage
    print("\n[Layer 3: Image Layers & Content-Addressable Storage]")
    images_count = run_cmd("docker images -q | wc -l")
    print(f"  Content-Addressable Blobs: {images_count} image tags registered.")
    print("  Storage: Rootfs tarballs hashed with SHA-256 and chained into immutable parent-child DAGs.")

    # 4. Container Execution Spec (OCI)
    print("\n[Layer 4: Container Execution Spec (OCI Bundle)]")
    print("  Spec: Docker daemon passes an OCI bundle (config.json + rootfs) to containerd / runc.")
    print("  runc translates the JSON spec into kernel syscalls (`clone()`, `unshare()`, `setns()`).")

    # 5. Linux Namespaces
    print("\n[Layer 5: Linux Namespaces (The Isolation Illusion)]")
    namespaces = [
        ("PID", "Isolates process IDs; process sees itself as PID 1."),
        ("Mount", "Isolates mount points; process sees isolated root filesystem."),
        ("Net", "Isolates network devices, routing tables, port bindings, loopback."),
        ("IPC", "Isolates System V IPC and POSIX message queues."),
        ("UTS", "Isolates hostname and NIS domain name."),
        ("User", "Maps container UID/GID to different host UID/GID."),
        ("Cgroup", "Isolates cgroup root hierarchy view.")
    ]
    for ns, desc in namespaces:
        print(f"  * {ns:8}: {desc}")

    # 6. Control Groups (cgroups)
    print("\n[Layer 6: Control Groups (cgroups v2 - Resource Governance)]")
    print("  Enforcement: Kernel throttles CPU (`cpu.max`), limits memory (`memory.max`), and prevents fork-bombs (`pids.max`).")

    # 7. OverlayFS (Copy-on-Write)
    print("\n[Layer 7: Storage Driver - OverlayFS (CoW)]")
    print("  lowerdir : Immutable read-only base layers stacked bottom-to-top.")
    print("  upperdir : Thin, read-write layer unique to this container instance.")
    print("  workdir  : Internal atomic transaction staging directory.")
    print("  merged   : Unified virtual directory presented to the container process.")

    # 8. Virtual Bridges & veth Pairs
    print("\n[Layer 8: Virtual Network Bridges & veth Pairs]")
    print("  Plumbing: Linux kernel creates a virtual ethernet pair (`veth` <-> `eth0`).")
    print("  Switching: Host end attaches to a virtual Linux bridge (`br-*` or `docker0`).")

    # 9. Embedded DNS Resolver
    print("\n[Layer 9: Embedded DNS (127.0.0.11)]")
    print("  Interception: `/etc/resolv.conf` directs queries to internal daemon DNS.")
    print("  Resolution: Maps service names ('postgres', 'redis') to dynamic container IPs.")

    # 10. Persistent Volumes
    print("\n[Layer 10: Persistent Volumes]")
    volumes_count = run_cmd("docker volume ls -q | wc -l")
    print(f"  Volumes: {volumes_count} named volumes managed in Docker host storage.")
    print("  Bypass: Volume directories completely bypass OverlayFS, writing directly to the host filesystem.")

    # 11. Port Publishing & NAT
    print("\n[Layer 11: Ports & NAT Publishing]")
    print("  Mechanisms: iptables DNAT rules rewrite inbound packets from host ports to container private IPs.")
    print("  Userland: `docker-proxy` forwards TCP streams across userland network interfaces.")

    # 12. PID 1 & Signal Traps
    print("\n[Layer 12: PID 1 & Signal Traps]")
    print("  Special Role: Reaps zombie orphan processes and traps POSIX signals (SIGTERM, SIGHUP).")
    print("  Init: Built-in `docker-init` (tini) ensures standard process hygiene.")

    # 13. Health Probes
    print("\n[Layer 13: Health Probes]")
    print("  Reconciliation: Daemon polls test probes and gates startup dependencies (`condition: service_healthy`).")

    # 14. Logs & Standard Streams
    print("\n[Layer 14: Logs & Standard Streams]")
    print("  Multiplexing: runc captures stdout (fd 1) and stderr (fd 2), streaming frames into JSON logs.")

    print("\n" + "=" * 80)
    print("WHAT EXACTLY EXISTS ON MY COMPUTER RIGHT NOW?")
    print("=" * 80)
    print("1. There is NO such physical object called a 'container'.")
    print("2. There are standard Linux processes executing code directly on CPU cores.")
    print("3. There are kernel data structures tagging those processes:")
    print("   - nsproxy struct: Points to namespaces defining what the process can SEE.")
    print("   - css_set struct: Points to cgroups defining what the process can USE.")
    print("4. There is a directory on disk mounted via overlayfs defining what the process can READ/WRITE.")
    print("5. There are virtual cables (veth pairs) defining how the process can COMMUNICATE.")
    print("=" * 80)

if __name__ == "__main__":
    main()
