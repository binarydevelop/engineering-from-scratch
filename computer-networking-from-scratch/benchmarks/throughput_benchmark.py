#!/usr/bin/env python3
"""
benchmarks/throughput_benchmark.py
Measures maximum TCP streaming throughput (MB/s and Gbps) across varying buffer chunk sizes.
"""

import socket
import threading
import time


def run_drain_server(port: int, total_bytes: int, stop_event: threading.Event):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("127.0.0.1", port))
        s.listen(1)
        conn, _ = s.accept()
        with conn:
            received = 0
            while received < total_bytes and not stop_event.is_set():
                chunk = conn.recv(65536)
                if not chunk:
                    break
                received += len(chunk)


def measure_throughput(chunk_size: int, total_bytes: int = 50 * 1024 * 1024) -> float:
    port = 9877
    stop = threading.Event()
    server_t = threading.Thread(target=run_drain_server, args=(port, total_bytes, stop), daemon=True)
    server_t.start()
    time.sleep(0.05)

    payload = b"X" * chunk_size
    sent = 0

    with socket.create_connection(("127.0.0.1", port)) as client:
        t0 = time.perf_counter()
        while sent < total_bytes:
            to_send = min(chunk_size, total_bytes - sent)
            client.sendall(payload[:to_send])
            sent += to_send
        t1 = time.perf_counter()

    stop.set()
    duration = t1 - t0
    mb_per_sec = (total_bytes / (1024 * 1024)) / duration
    return mb_per_sec


if __name__ == "__main__":
    print("TCP Socket Throughput Benchmark (50 MB transfer over loopback):")
    print("=" * 65)

    for chunk in [1024, 8192, 65536, 1048576]:
        rate = measure_throughput(chunk)
        gbps = (rate * 8) / 1024.0
        print(f"  Chunk Size: {chunk//1024:4d} KB -> Throughput: {rate:8.2f} MB/s ({gbps:6.2f} Gbps)")

    print("SUCCESS: Throughput benchmark completed.")
