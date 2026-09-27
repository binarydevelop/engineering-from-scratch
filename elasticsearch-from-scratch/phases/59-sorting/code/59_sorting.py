#!/usr/bin/env python3
import time

def benchmark_sorting(n=100000):
    # Simulated documents
    docs = [{"id": i, "price": (i * 37) % 1000, "score": (i * 17) % 100 / 10.0} for i in range(n)]

    # 1. Sort by score
    t0 = time.perf_counter()
    s1 = sorted(docs, key=lambda x: x["score"], reverse=True)[:10]
    t_score = (time.perf_counter() - t0) * 1000

    # 2. Sort by price
    t0 = time.perf_counter()
    s2 = sorted(docs, key=lambda x: x["price"])[:10]
    t_field = (time.perf_counter() - t0) * 1000

    return t_score, t_field

if __name__ == "__main__":
    t_s, t_f = benchmark_sorting(100000)
    print(f"Sort 100,000 items by score: {t_s:.2f} ms")
    print(f"Sort 100,000 items by price: {t_f:.2f} ms")
