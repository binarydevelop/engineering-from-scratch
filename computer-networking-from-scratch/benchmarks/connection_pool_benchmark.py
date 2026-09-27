#!/usr/bin/env python3
"""
benchmarks/connection_pool_benchmark.py
Demonstrates the substantial latency and CPU overhead of creating a new TCP connection
per request versus reusing a persistent connection pool (e.g. databases, HTTP Keep-Alive).
"""

import socket
import threading
import time


def run_simple_server(port: int, stop_event: threading.Event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(64)
        s.settimeout(0.5)

        while not stop_event.is_set():
            try:
                conn, _ = s.accept()
                with conn:
                    while not stop_event.is_set():
                        data = conn.recv(64)
                        if not data:
                            break
                        conn.sendall(b"OK")
            except socket.timeout:
                continue


def benchmark_new_connection_per_request(port: int, count: int = 200) -> float:
    t0 = time.perf_counter()
    for _ in range(count):
        with socket.create_connection(("127.0.0.1", port)) as s:
            s.sendall(b"Q")
            s.recv(64)
    return time.perf_counter() - t0


def benchmark_pooled_connection(port: int, count: int = 200) -> float:
    t0 = time.perf_counter()
    with socket.create_connection(("127.0.0.1", port)) as s:
        for _ in range(count):
            s.sendall(b"Q")
            s.recv(64)
    return time.perf_counter() - t0


if __name__ == "__main__":
    port = 9879
    stop = threading.Event()
    srv_thread = threading.Thread(target=run_simple_server, args=(port, stop), daemon=True)
    srv_thread.start()
    time.sleep(0.1)

    n_ops = 300
    print(f"Connection Pool vs. New Connection Per Request ({n_ops} operations):")
    print("=" * 65)

    time_new = benchmark_new_connection_per_request(port, count=n_ops)
    time_pool = benchmark_pooled_connection(port, count=n_ops)
    stop.set()

    print(f"  New TCP Connection Per Request: {time_new*1000:7.2f} ms ({time_new/n_ops*1000:.3f} ms/req)")
    print(f"  Reused Persistent Connection:    {time_pool*1000:7.2f} ms ({time_pool/n_ops*1000:.3f} ms/req)")
    print(f"  Speedup:                         {time_new / time_pool:7.1f}x faster!")
    print("SUCCESS: Connection pooling benchmark completed.")
