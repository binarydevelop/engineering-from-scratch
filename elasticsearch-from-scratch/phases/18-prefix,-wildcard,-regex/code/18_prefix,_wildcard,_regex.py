#!/usr/bin/env python3
import time
import bisect
import re

def build_sorted_terms(count=50000):
    terms = [f"item_{i:06d}_suffix" for i in range(count)]
    terms.append("elasticsearch_engine")
    terms.append("elastic_cloud")
    terms.sort()
    return terms

def prefix_search(terms, prefix):
    # O(log N) prefix scan
    start = bisect.bisect_left(terms, prefix)
    hits = []
    while start < len(terms) and terms[start].startswith(prefix):
        hits.append(terms[start])
        start += 1
    return hits

def regex_scan(terms, pattern_str):
    # O(N) full dictionary iteration
    rx = re.compile(pattern_str)
    return [t for t in terms if rx.search(t)]

if __name__ == "__main__":
    terms = build_sorted_terms(100000)
    
    t0 = time.perf_counter()
    p_hits = prefix_search(terms, "elastic")
    p_time = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    r_hits = regex_scan(terms, r".*search.*")
    r_time = (time.perf_counter() - t0) * 1000

    print(f"Prefix search 'elastic*':    {p_time:.4f} ms (Hits: {len(p_hits)})")
    print(f"Regex scan '.*search.*':     {r_time:.4f} ms (Hits: {len(r_hits)})")
    print(f"Prefix search was {r_time / p_time:.1f}x faster!")
