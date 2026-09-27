#!/usr/bin/env python3
import socket
import time
from statistics import median

def run_benchmark(n=5000):
    print(f"Measuring Redis Latency Percentiles ({n:,} operations)...")
    latencies = []
    try:
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t_start = time.perf_counter()
        for i in range(n):
            cmd = f"*3\r\n$3\r\nSET\r\n$8\r\nbench:{i}\r\n$5\r\nvalue\r\n".encode()
            t0 = time.perf_counter()
            s.sendall(cmd)
            _ = s.recv(1024)
            latencies.append((time.perf_counter() - t0) * 1000)
        total_time = time.perf_counter() - t_start
        s.close()

        latencies.sort()
        print(f"Total Time: {total_time:.3f}s | Throughput: {n/total_time:,.0f} ops/sec")
        print(f"  • p50 (Median) : {median(latencies):.3f} ms")
        print(f"  • p95          : {latencies[int(n*0.95)]:.3f} ms")
        print(f"  • p99          : {latencies[int(n*0.99)]:.3f} ms")
        print(f"  • Max Latency  : {latencies[-1]:.3f} ms")
    except Exception as e:
        print("Redis unavailable:", e)

if __name__ == "__main__":
    run_benchmark()
