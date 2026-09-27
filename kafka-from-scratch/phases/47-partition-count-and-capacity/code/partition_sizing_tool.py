#!/usr/bin/env python3
import math

def recommend_partitions(target_throughput_mb_s, consumer_speed_mb_s=2.5, producer_speed_mb_s=15.0, broker_count=3):
    print("=== Kafka Topic Partition Sizing Advisor ===\n")
    parts_for_consumer = math.ceil(target_throughput_mb_s / consumer_speed_mb_s)
    parts_for_producer = math.ceil(target_throughput_mb_s / producer_speed_mb_s)

    recommended = max(parts_for_consumer, parts_for_producer)
    # Align to a multiple of broker count for even distribution
    aligned = math.ceil(recommended / broker_count) * broker_count

    print(f"Target Throughput:           {target_throughput_mb_s:6.1f} MB/s")
    print(f"Single Consumer Capacity:    {consumer_speed_mb_s:6.1f} MB/s (DB-bound)")
    print(f"Single Producer Capacity:    {producer_speed_mb_s:6.1f} MB/s\n")
    print(f"Partitions for Consumer:     {parts_for_consumer}")
    print(f"Partitions for Producer:     {parts_for_producer}")
    print(f"Raw Recommended:             {recommended}")
    print(f"Aligned (Multiple of {broker_count} brokers): {aligned} partitions")

if __name__ == "__main__":
    recommend_partitions(target_throughput_mb_s=20.0, broker_count=3)
