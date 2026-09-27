#!/usr/bin/env python3
"""
benchmarks/latency_benchmark.py
Measures socket round-trip time (RTT) latency distributions (p50, p90, p99, min, max)
over loopback and network endpoints.
"""

import socket
import statistics
import threading
import time
from typing import List, Tuple


def run_echo_server(port: int, stop_event: threading.Event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(1)
        s.settimeout(0.5)

        while not stop_event.is_set():
            try:
                conn, _ = s.accept()
                with conn:
                    while not stop_event.is_set():
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(data)
            except socket.timeout:
                continue


def benchmark_latency(port: int, iterations: int = 1000) -> List[float]:
    latencies_ms = []
    with socket.create_connection(("127.0.0.1", port)) as s:
        # Disable Nagle's algorithm for pure latency measurement
        s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        payload = b"PING"

        for _ in range(iterations):
            t0 = time.perf_counter()
            s.sendall(payload)
            reply = s.recv(1024)
            t1 = time.perf_counter()
            latencies_ms.append((t1 - t0) * 1000.0)

    return latencies_ms


if __name__ == "__main__":
    test_port = 9876
    stop = threading.Event()
    server_thread = threading.Thread(target=run_echo_server, args=(test_port, stop), daemon=True)
    server_thread.start()
    time.sleep(0.1)

    print(f"Running Loopback Latency Benchmark (1,000 iterations)...")
    lats = benchmark_latency(test_port, iterations=1000)
    stop.set()

    lats_sorted = sorted(lats)
    p50 = statistics.median(lats_sorted)
    p90 = lats_sorted[int(len(lats_sorted) * 0.90)]
    p99 = lats_sorted[int(len(lats_sorted) * 0.99)]
    avg = statistics.mean(lats_sorted)

    print(f"Results:")
    print(f"  Min:  {min(lats):.4f} ms")
    print(f"  p50:  {p50:.4f} ms")
    print(f"  p90:  {p90:.4f} ms")
    print(f"  p99:  {p99:.4f} ms")
    print(f"  Max:  {max(lats):.4f} ms")
    print(f"  Mean: {avg:.4f} ms")
    print("SUCCESS: Latency benchmark completed.")
