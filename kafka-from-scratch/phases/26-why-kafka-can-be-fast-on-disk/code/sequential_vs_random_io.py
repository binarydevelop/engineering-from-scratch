#!/usr/bin/env python3
import time
import os
import random

def bench_io(total_writes=20000, record_size=128):
    payload = b"X" * record_size
    seq_path = "/tmp/bench_seq.dat"
    rand_path = "/tmp/bench_rand.dat"
    
    # 1. Sequential Appends
    start = time.time()
    with open(seq_path, "wb") as f:
        for _ in range(total_writes):
            f.write(payload)
    seq_dur = time.time() - start
    
    # 2. Random Seeks & Writes
    # Pre-allocate file
    with open(rand_path, "wb") as f:
        f.write(b"\0" * (total_writes * record_size))
        
    start = time.time()
    with open(rand_path, "r+b") as f:
        positions = list(range(total_writes))
        random.shuffle(positions)
        for pos in positions:
            f.seek(pos * record_size)
            f.write(payload)
    rand_dur = time.time() - start

    if os.path.exists(seq_path): os.remove(seq_path)
    if os.path.exists(rand_path): os.remove(rand_path)

    print(f"Sequential Appends: {total_writes/seq_dur:9.1f} writes/s ({seq_dur:.3f} s)")
    print(f"Random Seeks:       {total_writes/rand_dur:9.1f} writes/s ({rand_dur:.3f} s)")
    print(f"Sequential Advantage: {rand_dur/seq_dur:.1f}x faster!")

if __name__ == "__main__":
    bench_io()
