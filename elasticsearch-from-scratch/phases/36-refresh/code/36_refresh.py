#!/usr/bin/env python3
import time

def simulate_indexing(doc_count, refresh_every):
    segments = 0
    buffer = 0
    t0 = time.perf_counter()
    for i in range(doc_count):
        buffer += 1
        if refresh_every > 0 and buffer >= refresh_every:
            # Simulate segment flush overhead
            time.sleep(0.0005)
            segments += 1
            buffer = 0
    if buffer > 0:
        segments += 1
    elapsed = time.perf_counter() - t0
    return segments, elapsed

if __name__ == "__main__":
    docs = 5000
    print(f"Simulating Indexing {docs} documents:")
    s1, t1 = simulate_indexing(docs, refresh_every=50) # frequent refresh
    s2, t2 = simulate_indexing(docs, refresh_every=1000) # relaxed refresh
    print(f"Frequent Refresh (every 50 docs):   {s1} segments, {t1:.3f}s ({docs/t1:.0f} docs/sec)")
    print(f"Relaxed Refresh  (every 1000 docs): {s2} segments, {t2:.3f}s ({docs/t2:.0f} docs/sec)")
