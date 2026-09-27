#!/usr/bin/env python3
import json
import gzip
import zlib

def test_compression_ratios():
    sample_record = {
        "event_type": "USER_CLICK_EVENT",
        "service": "checkout-frontend-production",
        "user_id": "usr_998124871",
        "ip_address": "192.168.1.105",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "attributes": {"campaign": "autumn_sale_2026", "item_id": "SKU-9901-XL"}
    }
    raw_json = json.dumps(sample_record).encode("utf-8")

    # 1. Single record compression
    compressed_single = gzip.compress(raw_json)

    # 2. Batch of 100 identical/similar records
    raw_batch = b"".join([json.dumps(dict(sample_record, event_id=f"evt_{i}")).encode("utf-8") for i in range(100)])
    compressed_batch = gzip.compress(raw_batch)

    print(f"Single Record Raw:        {len(raw_json):5d} bytes")
    print(f"Single Record Compressed: {len(compressed_single):5d} bytes (Ratio: {len(compressed_single)/len(raw_json):.2f})\n")

    print(f"Batch of 100 Records Raw: {len(raw_batch):5d} bytes")
    print(f"Batch Compressed:         {len(compressed_batch):5d} bytes (Ratio: {len(compressed_batch)/len(raw_batch):.2f})")
    print(f"\nBatch Space Savings: {100 - (len(compressed_batch)/len(raw_batch)*100):.1f}% reduction!")

if __name__ == "__main__":
    test_compression_ratios()
