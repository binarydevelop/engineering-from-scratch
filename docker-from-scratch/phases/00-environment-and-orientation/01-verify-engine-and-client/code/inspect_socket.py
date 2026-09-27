#!/usr/bin/env python3
"""
inspect_socket.py
Communicates directly with the Docker Engine daemon over the Unix Domain Socket
using standard HTTP. Proves that 'docker' CLI is merely an HTTP REST client.
"""

import http.client
import json
import socket
import sys
import os

DOCKER_SOCKET = "/var/run/docker.sock"

class UnixSocketConnection(http.client.HTTPConnection):
    def __init__(self, socket_path):
        super().__init__("localhost")
        self.socket_path = socket_path

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.socket_path)

def query_docker_api(endpoint: str) -> dict:
    if not os.path.exists(DOCKER_SOCKET):
        print(f"Error: Docker socket '{DOCKER_SOCKET}' does not exist.", file=sys.stderr)
        print("Ensure Docker Desktop or dockerd is running.", file=sys.stderr)
        sys.exit(1)
        
    conn = UnixSocketConnection(DOCKER_SOCKET)
    conn.request("GET", endpoint, headers={"Host": "localhost"})
    response = conn.getresponse()
    
    if response.status != 200:
        print(f"HTTP Error {response.status}: {response.reason}", file=sys.stderr)
        sys.exit(1)
        
    data = json.loads(response.read().decode("utf-8"))
    conn.close()
    return data

def main():
    print("=== Direct Docker Daemon API Query (via Unix Socket) ===")
    print(f"Connecting to Unix Socket: {DOCKER_SOCKET}\n")
    
    version_data = query_docker_api("/version")
    print(f"Docker API Version: {version_data.get('ApiVersion')}")
    print(f"Engine Version:     {version_data.get('Version')}")
    print(f"Kernel Version:     {version_data.get('KernelVersion')}")
    print(f"OS/Architecture:    {version_data.get('Os')}/{version_data.get('Arch')}")
    print(f"Components:")
    for comp in version_data.get('Components', []):
        print(f"  - {comp.get('Name')}: v{comp.get('Version')}")
        
    info_data = query_docker_api("/info")
    print("\nEngine Telemetry:")
    print(f"  Total Containers: {info_data.get('Containers', 0)}")
    print(f"  Running:          {info_data.get('ContainersRunning', 0)}")
    print(f"  Paused:           {info_data.get('ContainersPaused', 0)}")
    print(f"  Stopped:          {info_data.get('ContainersStopped', 0)}")
    print(f"  Total Images:     {info_data.get('Images', 0)}")
    print(f"  Storage Driver:   {info_data.get('Driver', 'unknown')}")
    print(f"  Server Version:   {info_data.get('ServerVersion')}")

if __name__ == "__main__":
    main()
