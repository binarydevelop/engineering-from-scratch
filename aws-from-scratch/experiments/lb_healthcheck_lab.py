#!/usr/bin/env python3
"""
experiments/lb_healthcheck_lab.py
Phases 22 & 23: Load Balancing From Scratch, Health Checks & Target Group Eviction

This script simulates an Application Load Balancer (ALB) reverse proxy in pure Python:
  1. Target Group: Manages multiple backend instances (Instance A, Instance B).
  2. Health Checks: Periodically probes backend targets on /health.
  3. Failure Injection: Simulates target crash / 500 status.
  4. Health Eviction: Removes failed target after consecutive threshold failures.
  5. Recovery: Re-integrates target after consecutive threshold successes.
  6. Zero-Downtime Failover: Measures client availability during outage.
"""

import time
from typing import Dict, List, Optional


class BackendTarget:
    def __init__(self, instance_id: str, az: str, ip: str, port: int):
        self.instance_id = instance_id
        self.az = az
        self.ip = ip
        self.port = port
        self.app_healthy = True  # Instance's real application health state
        self.is_healthy = True   # ALB's perception after threshold checks
        self.is_alive = True     # Process alive/dead (TCP connection)
        self.consecutive_passes = 0
        self.consecutive_fails = 0
        self.total_requests_served = 0

    def handle_request(self, path: str) -> Dict[str, Any]:
        if not self.is_alive:
            raise ConnectionRefusedError(f"Connection refused to {self.ip}:{self.port}")
        
        self.total_requests_served += 1
        if path == "/health":
            return {"status": 200, "body": "OK"} if self.app_healthy else {"status": 500, "body": "ERROR"}
        
        if not self.app_healthy:
            return {"status": 500, "body": "Internal Server Error"}
        
        return {
            "status": 200,
            "body": f"Handled by {self.instance_id} in {self.az} ({self.ip})"
        }


class LoadBalancerTargetGroup:
    def __init__(self, name: str, health_check_path: str = "/health", healthy_threshold: int = 2, unhealthy_threshold: int = 2):
        self.name = name
        self.health_check_path = health_check_path
        self.healthy_threshold = healthy_threshold
        self.unhealthy_threshold = unhealthy_threshold
        self.targets: List[BackendTarget] = []
        self._round_robin_idx = 0

    def register_target(self, target: BackendTarget):
        self.targets.append(target)

    def probe_health_checks(self):
        """Simulates periodic background ALB health check pings."""
        print("  [ALB HEALTH CHECK PROBE]")
        for t in self.targets:
            status = "HEALTHY"
            try:
                res = t.handle_request(self.health_check_path)
                if res["status"] == 200:
                    t.consecutive_passes += 1
                    t.consecutive_fails = 0
                    if t.consecutive_passes >= self.healthy_threshold:
                        t.is_healthy = True
                else:
                    t.consecutive_fails += 1
                    t.consecutive_passes = 0
                    if t.consecutive_fails >= self.unhealthy_threshold:
                        t.is_healthy = False
            except Exception:
                t.consecutive_fails += 1
                t.consecutive_passes = 0
                if t.consecutive_fails >= self.unhealthy_threshold:
                    t.is_healthy = False

            state_desc = "HEALTHY" if t.is_healthy else "UNHEALTHY"
            print(f"    Target {t.instance_id} ({t.ip}): Status={state_desc} (Passes: {t.consecutive_passes}, Fails: {t.consecutive_fails})")

    def forward_request(self, path: str) -> Dict[str, Any]:
        """Routes request to next healthy target in target group."""
        healthy_pool = [t for t in self.targets if t.is_healthy and t.is_alive]
        if not healthy_pool:
            return {
                "status": 503,
                "body": "HTTP 503 Service Unavailable: No healthy targets in target group."
            }

        target = healthy_pool[self._round_robin_idx % len(healthy_pool)]
        self._round_robin_idx += 1
        return target.handle_request(path)


def run_experiment():
    print("=" * 65)
    print("     ALB Target Group & Health Check Simulation Lab              ")
    print("=" * 65)

    tg = LoadBalancerTargetGroup("app-tg-prod", healthy_threshold=2, unhealthy_threshold=2)
    inst_a = BackendTarget("i-001a", "us-east-1a", "10.0.1.50", 8080)
    inst_b = BackendTarget("i-002b", "us-east-1b", "10.0.2.60", 8080)

    tg.register_target(inst_a)
    tg.register_target(inst_b)

    # Initial state
    print("\n--- Phase 1: Baseline Round-Robin Distribution ---")
    tg.probe_health_checks()
    for req_num in range(1, 7):
        resp = tg.forward_request("/api/orders")
        print(f"  Request #{req_num}: {resp['body']}")

    print(f"Requests served -> Instance A: {inst_a.total_requests_served}, Instance B: {inst_b.total_requests_served}")

    # Inject failure on Instance A
    print("\n--- Phase 2: Failure Injection on Instance A (i-001a) ---")
    print("Simulating application crash / database disconnect on i-001a...")
    inst_a.is_alive = False  # Crashed process (TCP RST / Connection refused)

    print("\nCheck 1 after crash:")
    tg.probe_health_checks()

    print("\nCheck 2 after crash (Threshold of 2 reached -> Eviction):")
    tg.probe_health_checks()

    # Route traffic during failure
    print("\n--- Phase 3: Traffic Routing During Instance A Failure ---")
    for req_num in range(7, 13):
        resp = tg.forward_request("/api/orders")
        print(f"  Request #{req_num}: {resp['body']}")

    print(f"Requests served -> Instance A: {inst_a.total_requests_served}, Instance B: {inst_b.total_requests_served}")
    print("Notice: 100% of client traffic seamlessly redirected to Instance B! Zero 5xx errors for clients.")

    # Recover Instance A
    print("\n--- Phase 4: Recovering Instance A (Self-Healing / Restart) ---")
    print("Restarting application service on i-001a...")
    inst_a.is_alive = True
    inst_a.app_healthy = True
    inst_a.consecutive_passes = 0
    inst_a.consecutive_fails = 0
    inst_a.is_healthy = False  # Needs to pass healthy threshold first

    print("\nRecovery Probe 1:")
    tg.probe_health_checks()

    print("\nRecovery Probe 2 (Healthy threshold of 2 reached -> Re-added to pool):")
    tg.probe_health_checks()

    # Post-recovery traffic distribution
    print("\n--- Phase 5: Post-Recovery Traffic Distribution ---")
    for req_num in range(13, 17):
        resp = tg.forward_request("/api/orders")
        print(f"  Request #{req_num}: {resp['body']}")

    print("\n" + "=" * 65)
    print("First-Principles Realization:")
    print("An ALB is not magic: it is a reverse proxy with continuous active")
    print("health probes that updates its internal routing table dynamically.")
    print("=" * 65)


if __name__ == "__main__":
    run_experiment()
