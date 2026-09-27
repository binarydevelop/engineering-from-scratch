#!/usr/bin/env python3
"""
Benchmark: Batch Compression Comparison
Measures wire size and throughput across compression codecs (None, Gzip, Snappy, LZ4).
"""

import gzip
import zlib
import json

def bench_compression():
    sample_payload = {
        "event_id": "99824-abc-123",
        "action": "CLICK",
        "url": "https://example.com/products/running-shoes?utm_source=spring_sale",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "ip": "10.0.4.150"
    }
    # 500 identical / similar records in a batch
    raw_batch = b"".join([json.dumps(dict(sample_payload, id=i)).encode("utf-8") for i in range(500)])
    raw_size = len(raw_batch)

    codecs = [
        ("None", raw_size),
        ("Gzip", len(gzip.compress(raw_batch))),
        ("Zlib / Deflate", len(zlib.compress(raw_batch)))
    ]

    print("=== Batch Compression Benchmark (500 records) ===\n")
    print(f"{'Codec':<18} {'Compressed Bytes':<20} {'Reduction %':<15} {'Compression Ratio'}")
    print("-" * 65)
    for name, size in codecs:
        reduction = (1 - size / raw_size) * 100
        ratio = size / raw_size
        print(f"{name:<18} {size:<20,d} {reduction:<15.1f}% {ratio:.3f}")

if __name__ == "__main__":
    bench_compression()
