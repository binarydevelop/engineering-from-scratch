#!/usr/bin/env python3
import time

def simulate_from_size(data, from_offset, size):
    # Simulates sorting and discarding
    sorted_data = sorted(data, key=lambda x: x["val"], reverse=True)
    return sorted_data[from_offset:from_offset + size]

def simulate_search_after(data, last_val, last_id, size):
    # Direct cursor filtering
    candidates = [d for d in data if (d["val"] < last_val) or (d["val"] == last_val and d["id"] > last_id)]
    sorted_candidates = sorted(candidates, key=lambda x: (-x["val"], x["id"]))
    return sorted_candidates[:size]

if __name__ == "__main__":
    items = [{"id": i, "val": 100000 - i} for i in range(50000)]
    t0 = time.perf_counter()
    p1 = simulate_from_size(items, from_offset=40000, size=10)
    t_from = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    p2 = simulate_search_after(items, last_val=60001, last_id=39999, size=10)
    t_cursor = (time.perf_counter() - t0) * 1000

    print(f"Deep Paging (from=40000): {t_from:.2f} ms")
    print(f"Cursor (search_after):    {t_cursor:.2f} ms")
    print(f"Cursor pagination was {t_from / t_cursor:.1f}x faster!")
