#!/usr/bin/env python3
from collections import defaultdict

def bucket_terms(docs, field):
    buckets = defaultdict(int)
    for d in docs:
        val = d.get(field)
        if val is not None:
            buckets[val] += 1
    return dict(sorted(buckets.items(), key=lambda x: x[1], reverse=True))

def bucket_range(docs, field, ranges):
    # ranges: list of (label, min_val, max_val)
    bucket_counts = {r[0]: 0 for r in ranges}
    for d in docs:
        val = d.get(field)
        if val is not None:
            for label, low, high in ranges:
                if (low is None or val >= low) and (high is None or val < high):
                    bucket_counts[label] += 1
                    break
    return bucket_counts

if __name__ == "__main__":
    docs = [
        {"cat": "books", "price": 25},
        {"cat": "books", "price": 45},
        {"cat": "tech", "price": 150},
        {"cat": "tech", "price": 500},
        {"cat": "home", "price": 80}
    ]
    print("Terms Buckets (cat):", bucket_terms(docs, "cat"))
    price_ranges = [("under_50", None, 50), ("50_to_200", 50, 200), ("over_200", 200, None)]
    print("Range Buckets (price):", bucket_range(docs, "price", price_ranges))
