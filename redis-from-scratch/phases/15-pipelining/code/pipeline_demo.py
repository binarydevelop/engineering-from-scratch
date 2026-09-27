#!/usr/bin/env python3
import socket
import time

def run_pipelining_experiment(n=2000):
    print(f"Comparing Sequential RTT vs Pipelined Batch ({n:,} operations)...")
    try:
        # 1. Sequential
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t0 = time.perf_counter()
        for i in range(n):
            s.sendall(f"*3\r\n$3\r\nSET\r\n$7\r\nseq_k{i}\r\n$1\r\nv\r\n".encode())
            _ = s.recv(1024)
        seq_time = time.perf_counter() - t0
        s.close()

        # 2. Pipelined (batch size 50)
        batch_size = 50
        s = socket.create_connection(("localhost", 6379), timeout=5.0)
        t0 = time.perf_counter()
        for b in range(0, n, batch_size):
            buf = "".join(f"*3\r\n$3\r\nSET\r\n$7\r\npip_k{i}\r\n$1\r\nv\r\n" for i in range(b, b + batch_size))
            s.sendall(buf.encode())
            rec = 0
            while rec < batch_size * 5: # +OK\r\n is 5 bytes
                data = s.recv(4096)
                rec += len(data)
        pipe_time = time.perf_counter() - t0
        s.close()

        print(f"  • Sequential (1 RTT/op) : {seq_time:.3f}s ({n/seq_time:8,.0f} ops/sec)")
        print(f"  • Pipelined (batch 50)  : {pipe_time:.3f}s ({n/pipe_time:8,.0f} ops/sec)")
        print(f"  -> Speedup: {seq_time/pipe_time:.1f}x faster throughput via pipelining!")
    except Exception as e:
        print("Redis unavailable:", e)

if __name__ == "__main__":
    run_pipelining_experiment()
