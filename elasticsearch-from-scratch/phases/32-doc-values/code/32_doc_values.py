#!/usr/bin/env python3
import time

def generate_row_store(n=100000):
    return [{"id": i, "price": (i % 100) * 1.5, "tag": f"tag_{i%10}"} for i in range(n)]

def generate_column_store(rows):
    return [r["price"] for r in rows]

if __name__ == "__main__":
    rows = generate_row_store(100000)
    cols = generate_column_store(rows)

    # Summing across rows
    t0 = time.perf_counter()
    s1 = sum(r["price"] for r in rows)
    t_row = (time.perf_counter() - t0) * 1000

    # Summing contiguous column
    t0 = time.perf_counter()
    s2 = sum(cols)
    t_col = (time.perf_counter() - t0) * 1000

    print(f"Row iteration sum:    {t_row:.2f} ms")
    print(f"Column iteration sum: {t_col:.2f} ms")
    print(f"Columnar access was {t_row / t_col:.1f}x faster!")
