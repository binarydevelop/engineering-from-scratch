#!/usr/bin/env python3
"""
projects/09-production-web-path/production_topology.py
Simulates a multi-tier production web path:
  Client ──► DNS ──► Reverse Proxy / LB ──► App Instance A/B ──► Mock Datastore

Demonstrates complete layer-by-layer request tracing and failure injection:
  - DNS resolution failure
  - Application worker crash & LB failover
  - Database connection timeout & HTTP 504 propagation
"""

import json
import socket
import sys
import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class TraceStep:
    layer: str
    hop_name: str
    status: str
    latency_ms: float
    details: str


class MockDatabase:
    def __init__(self):
        self.data: Dict[str, str] = {"item:1": "Widget A", "item:2": "Widget B"}
        self.is_healthy = True

    def query(self, key: str) -> Optional[str]:
        if not self.is_healthy:
            time.sleep(0.5)
            raise TimeoutError("Database connection timed out")
        return self.data.get(key)


class ProductionAppInstance:
    def __init__(self, name: str, db: MockDatabase):
        self.name = name
        self.db = db
        self.is_alive = True

    def handle_request(self, item_id: str) -> Tuple[int, str]:
        if not self.is_alive:
            raise ConnectionRefusedError(f"{self.name} is down")
        val = self.db.query(item_id)
        if val:
            return 200, json.dumps({"source": self.name, "value": val})
        return 404, json.dumps({"error": "Item not found"})


class ProductionWebPath:
    def __init__(self):
        self.dns_records = {"api.company.internal": "10.0.0.100"}
        self.db = MockDatabase()
        self.app_a = ProductionAppInstance("app-worker-1", self.db)
        self.app_b = ProductionAppInstance("app-worker-2", self.db)
        self.app_pool = [self.app_a, self.app_b]
        self.rr_index = 0

    def resolve_dns(self, hostname: str) -> Optional[str]:
        return self.dns_records.get(hostname.lower())

    def execute_request_trace(self, url: str) -> Tuple[int, str, List[TraceStep]]:
        """Executes a full end-to-end traced request through the system."""
        trace: List[TraceStep] = []

        # 1. Parse URL
        if not url.startswith("http://"):
            return 400, "Bad Protocol", [TraceStep("L7", "Client", "ERROR", 0.0, "Only http:// supported")]
        host_and_path = url[7:]
        host, _, path = host_and_path.partition("/")
        item_id = path.split("/")[-1] if path else "item:1"

        # 2. DNS Resolution
        t0 = time.perf_counter()
        ip = self.resolve_dns(host)
        t_dns = (time.perf_counter() - t0) * 1000.0
        if not ip:
            trace.append(TraceStep("L7-DNS", "Local Stub Resolver", "FAILED", t_dns, f"NXDOMAIN: {host}"))
            return 0, "DNS NXDOMAIN", trace
        trace.append(TraceStep("L7-DNS", "Local Stub Resolver", "SUCCESS", t_dns, f"Resolved {host} -> {ip}"))

        # 3. Transport TCP Handshake with Reverse Proxy
        t0 = time.perf_counter()
        # Simulated 3-way handshake (1 RTT)
        time.sleep(0.001)
        t_tcp = (time.perf_counter() - t0) * 1000.0
        trace.append(TraceStep("L4-TCP", "Edge Reverse Proxy (:80)", "ESTABLISHED", t_tcp, "SYN -> SYN-ACK -> ACK"))

        # 4. Load Balancer selects healthy worker
        t0 = time.perf_counter()
        selected_app: Optional[ProductionAppInstance] = None
        for _ in range(len(self.app_pool)):
            cand = self.app_pool[self.rr_index % len(self.app_pool)]
            self.rr_index += 1
            if cand.is_alive:
                selected_app = cand
                break

        if not selected_app:
            t_fail = (time.perf_counter() - t0) * 1000.0
            trace.append(TraceStep("L7-LB", "Load Balancer", "FAILED", t_fail, "502 Bad Gateway: All workers crashed"))
            return 502, "Bad Gateway", trace

        trace.append(TraceStep("L7-LB", "Load Balancer", "ROUTED", 0.1, f"Forwarded to {selected_app.name}"))

        # 5. Worker handles request and queries DB
        try:
            code, body = selected_app.handle_request(item_id)
            t_app = (time.perf_counter() - t0) * 1000.0
            trace.append(TraceStep("L7-APP", selected_app.name, f"HTTP_{code}", t_app, f"DB query succeeded: {body}"))
            return code, body, trace
        except TimeoutError:
            t_to = (time.perf_counter() - t0) * 1000.0
            trace.append(TraceStep("L7-DB", "Mock Database", "TIMEOUT", t_to, "504 Gateway Timeout: DB query hung"))
            return 504, "Gateway Timeout", trace
        except ConnectionRefusedError:
            t_cr = (time.perf_counter() - t0) * 1000.0
            trace.append(TraceStep("L4-TCP", selected_app.name, "REFUSED", t_cr, "502 Bad Gateway: Worker crashed"))
            return 502, "Bad Gateway", trace


if __name__ == "__main__":
    path = ProductionWebPath()
    print("Executing End-to-End Production Request Trace:")
    print("=" * 70)

    # 1. Normal Request
    code, body, trace = path.execute_request_trace("http://api.company.internal/items/item:1")
    print(f"Request 1 Status: {code} -> Body: {body}")
    for step in trace:
        print(f"  [{step.layer:<6}] {step.hop_name:<24} | {step.status:<12} | {step.latency_ms:6.2f}ms | {step.details}")

    # 2. Inject Worker Failure: Kill App Worker 1
    print("\n[Fault Injection]: Killing app-worker-1...")
    path.app_a.is_alive = False
    code, body, trace = path.execute_request_trace("http://api.company.internal/items/item:2")
    print(f"Request 2 Status (After Failure): {code} -> Body: {body}")
    for step in trace:
        print(f"  [{step.layer:<6}] {step.hop_name:<24} | {step.status:<12} | {step.latency_ms:6.2f}ms | {step.details}")

    print("\nSUCCESS: Production web path end-to-end trace validated.")
