#!/usr/bin/env python3
"""
Benchmark Client for Capstone 5 HTTP Server
Sends concurrent HTTP requests to measure requests/sec and latency.
"""

import sys
import time
import socket
import threading
from typing import List


def send_single_request(host: str, port: int) -> float:
    start = time.perf_counter()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        req = b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
        s.sendall(req)
        resp = b""
        while True:
            chunk = s.recv(1024)
            if not chunk:
                break
            resp += chunk
    end = time.perf_counter()
    return (end - start) * 1000.0  # in ms


def run_benchmark(host: str = "127.0.0.1", port: int = 8080, num_requests: int = 500, concurrency: int = 10):
    latencies: List[float] = []
    lock = threading.Lock()

    def worker(count: int):
        local_lats = []
        for _ in range(count):
            try:
                lat = send_single_request(host, port)
                local_lats.append(lat)
            except Exception as e:
                pass
        with lock:
            latencies.extend(local_lats)

    threads = []
    req_per_thread = num_requests // concurrency
    t_start = time.perf_counter()

    for _ in range(concurrency):
        t = threading.Thread(target=worker, args=(req_per_thread,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    t_end = time.perf_counter()
    total_time = t_end - t_start

    if not latencies:
        print("Error: No requests completed successfully.")
        return

    latencies.sort()
    rps = len(latencies) / total_time
    p50 = latencies[len(latencies) // 2]
    p95 = latencies[int(len(latencies) * 0.95)]
    p99 = latencies[int(len(latencies) * 0.99)]

    print(f"================================================================")
    print(f"HTTP Server Benchmark Results ({host}:{port})")
    print(f"Concurrency: {concurrency} | Total Requests: {len(latencies)}")
    print(f"================================================================")
    print(f"Throughput:         {rps:.1f} requests/sec")
    print(f"Wall Clock Time:    {total_time:.3f} s")
    print(f"Latency (p50):      {p50:.2f} ms")
    print(f"Latency (p95):      {p95:.2f} ms")
    print(f"Latency (p99):      {p99:.2f} ms")
    print(f"================================================================")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    run_benchmark(port=port)
