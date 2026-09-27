#!/usr/bin/env python3
"""
projects/07-load-balancer/load_balancer.py
An advanced Layer-7 Load Balancer supporting multiple balancing algorithms:
  1. Round-Robin
  2. Least-Connections (tracks active in-flight requests per backend)
  3. IP Hash (consistent client IP mapping)
Demonstrates how Least-Connections protects systems when one backend slows down.
"""

import hashlib
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class UpstreamNode:
    host: str
    port: int
    active_connections: int = 0
    total_handled: int = 0
    is_alive: bool = True


class LoadBalancer:
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8080,
        algorithm: str = "ROUND_ROBIN",
        nodes: Optional[List[Tuple[str, int]]] = None,
        bind_listener: bool = True,
    ):
        self.host = host
        self.port = port
        self.algorithm = algorithm.upper()
        node_tuples = nodes or [("127.0.0.1", 8001), ("127.0.0.1", 8002)]
        self.nodes = [UpstreamNode(h, p) for h, p in node_tuples]
        self.rr_index = 0
        self.lock = threading.Lock()
        self.running = True

        self.listener: Optional[socket.socket] = None
        if bind_listener:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.listener.bind((self.host, self.port))
            self.listener.listen(128)

    def select_node(self, client_ip: str) -> Optional[UpstreamNode]:
        """Selects upstream node according to configured algorithm."""
        with self.lock:
            alive = [n for n in self.nodes if n.is_alive]
            if not alive:
                return None

            if self.algorithm == "LEAST_CONNECTIONS":
                # Pick node with lowest active_connections
                selected = min(alive, key=lambda n: n.active_connections)
            elif self.algorithm == "IP_HASH":
                # Hash client IP
                h = int(hashlib.md5(client_ip.encode()).hexdigest(), 16)
                selected = alive[h % len(alive)]
            else:  # ROUND_ROBIN
                selected = alive[self.rr_index % len(alive)]
                self.rr_index += 1

            selected.active_connections += 1
            selected.total_handled += 1
            return selected

    def release_node(self, node: UpstreamNode):
        with self.lock:
            node.active_connections = max(0, node.active_connections - 1)

    def handle_client(self, client_conn: socket.socket, client_addr):
        client_ip = client_addr[0]
        node = self.select_node(client_ip)
        if not node:
            client_conn.sendall(b"HTTP/1.1 503 Service Unavailable\r\n\r\n")
            return

        try:
            req = client_conn.recv(4096)
            if req:
                with socket.create_connection((node.host, node.port), timeout=5.0) as backend_sock:
                    backend_sock.sendall(req)
                    while True:
                        res = backend_sock.recv(4096)
                        if not res:
                            break
                        client_conn.sendall(res)
        except Exception:
            pass
        finally:
            self.release_node(node)

    def run(self):
        print(f"Load Balancer ({self.algorithm}) running on http://{self.host}:{self.port}")
        for n in self.nodes:
            print(f"  Backend Node: http://{n.host}:{n.port}")

        try:
            while self.running:
                conn, addr = self.listener.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr), daemon=True).start()
        except Exception:
            pass
        finally:
            self.close()

    def close(self):
        self.running = False
        if self.listener:
            try:
                self.listener.close()
            except Exception:
                pass


if __name__ == "__main__":
    algo = sys.argv[1] if len(sys.argv) > 1 else "ROUND_ROBIN"
    p = int(sys.argv[2]) if len(sys.argv) > 2 else 8080
    lb = LoadBalancer(port=p, algorithm=algo)
    lb.run()
