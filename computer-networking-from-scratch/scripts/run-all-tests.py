#!/usr/bin/env python3
"""
scripts/run-all-tests.py
The master test runner executing all simulation, socket, benchmark, and project test suites.
"""

import os
import subprocess
import sys
import time

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

TEST_SUITES = [
    ("Simulations Test Suite", ["python3", "-m", "unittest", "simulations/test_simulations.py"]),
    ("Broken Networks Catalog & Diagnostic Verifier", ["python3", "broken-networks/verify_all_broken_labs.py"]),
    ("Project 01: Raw TCP Chat Server", ["python3", "projects/01-raw-tcp-chat/test_chat.py"]),
    ("Project 02: HTTP/1.1 Server From Scratch", ["python3", "projects/02-http-server/test_http.py"]),
    ("Project 03: RFC 1035 UDP DNS Server", ["python3", "projects/03-dns-resolver/test_dns.py"]),
    ("Project 04: Router Forwarding Simulator", ["python3", "projects/04-router-simulator/test_router.py"]),
    ("Project 05: Reliable Transport Protocol", ["python3", "projects/05-reliable-transport/test_transport.py"]),
    ("Project 06: HTTP Reverse Proxy", ["python3", "projects/06-reverse-proxy/test_proxy.py"]),
    ("Project 07: L7 Load Balancer", ["python3", "projects/07-load-balancer/test_lb.py"]),
    ("Project 08: Tiny Internet Multi-Hop Routing", ["python3", "projects/08-tiny-internet/verify_tiny_internet.py"]),
    ("Project 09: Production Web Path & Incident Tracer", ["python3", "projects/09-production-web-path/test_production_path.py"]),
    ("Benchmark: Latency Distribution", ["python3", "benchmarks/latency_benchmark.py"]),
    ("Benchmark: Pipelining Acceleration", ["python3", "benchmarks/pipelining_benchmark.py"]),
    ("Benchmark: Connection Pooling", ["python3", "benchmarks/connection_pool_benchmark.py"]),
]


def run_all():
    print("=" * 75)
    print("   computer-networking-from-scratch Global Test & Validation Suite")
    print("=" * 75)

    passed = 0
    failed = 0
    t_start = time.perf_counter()

    for name, cmd in TEST_SUITES:
        print(f"\n[RUNNING] {name}...")
        res = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"[PASSED]  {name}")
            passed += 1
        else:
            print(f"[FAILED]  {name}")
            print("--- STDOUT ---")
            print(res.stdout)
            print("--- STDERR ---")
            print(res.stderr)
            failed += 1

    # Check C Compilation if compiler exists
    has_cc = subprocess.run(["which", "gcc"], capture_output=True).returncode == 0 or \
             subprocess.run(["which", "clang"], capture_output=True).returncode == 0
    if has_cc:
        print("\n[RUNNING] C Socket Programs Build & Test...")
        res = subprocess.run(["make", "-C", "socket-programs/c", "all"], cwd=REPO_ROOT, capture_output=True, text=True)
        if res.returncode == 0:
            subprocess.run(["make", "-C", "socket-programs/c", "clean"], cwd=REPO_ROOT, capture_output=True, text=True)
            print("[PASSED]  C Socket Programs Build")
            passed += 1
        else:
            print("[FAILED]  C Socket Programs Build")
            failed += 1

    duration = time.perf_counter() - t_start
    print("\n" + "=" * 75)
    print(f"Test Summary: {passed} PASSED, {failed} FAILED in {duration:.2f}s")
    print("=" * 75)

    if failed > 0:
        sys.exit(1)
    else:
        print("ALL TESTS AND VERIFICATIONS PASSED CLEANLY!")


if __name__ == "__main__":
    run_all()
