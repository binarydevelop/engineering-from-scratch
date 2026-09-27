#!/usr/bin/env python3
def calculate_kafka_capacity(
    events_per_sec=20000,
    bytes_per_event=1024,
    retention_days=7,
    replication_factor=3,
    consumer_groups=3,
    compression_ratio=0.5, # 50% size after LZ4/ZSTD
    num_brokers=6
):
    print("=== Apache Kafka Production Capacity Sizing Model ===\n")
    
    # 1. Raw Ingestion
    raw_bytes_per_sec = events_per_sec * bytes_per_event
    wire_bytes_per_sec = raw_bytes_per_sec * compression_ratio
    wire_mb_per_sec = wire_bytes_per_sec / (1024 * 1024)
    
    # 2. Daily Volume
    daily_wire_tb = (wire_bytes_per_sec * 86400) / (1024**4)
    
    # 3. Total Storage (with Replication & 30% Headroom)
    total_storage_tb = daily_wire_tb * retention_days * replication_factor * 1.3
    disk_per_broker_tb = total_storage_tb / num_brokers
    
    # 4. Network Bandwidth
    # Ingress = Producer Ingress + Follower Replication Ingress
    ingress_mb_per_sec = wire_mb_per_sec + (wire_mb_per_sec * (replication_factor - 1))
    # Egress = Follower Replication Egress + Consumer Groups Egress
    egress_mb_per_sec = (wire_mb_per_sec * (replication_factor - 1)) + (wire_mb_per_sec * consumer_groups)

    print(f"Input Parameters:")
    print(f"  Events/sec:          {events_per_sec:,}")
    print(f"  Event Size (Raw):    {bytes_per_event:,} bytes")
    print(f"  Compression Ratio:   {compression_ratio*100:.0f}%")
    print(f"  Retention:           {retention_days} days")
    print(f"  Replication Factor:  {replication_factor}")
    print(f"  Brokers Count:       {num_brokers}")
    print(f"  Consumer Groups:     {consumer_groups}\n")

    print(f"Storage Requirements:")
    print(f"  Daily Volume (Wire): {daily_wire_tb:6.2f} TB/day")
    print(f"  Total Replicated:    {total_storage_tb:6.2f} TB (including 30% safety headroom)")
    print(f"  Disk per Broker:     {disk_per_broker_tb:6.2f} TB / broker\n")

    print(f"Network Throughput Requirements:")
    print(f"  Cluster Ingress:     {ingress_mb_per_sec:6.1f} MB/s ({ingress_mb_per_sec*8:6.1f} Mbps)")
    print(f"  Cluster Egress:      {egress_mb_per_sec:6.1f} MB/s ({egress_mb_per_sec*8:6.1f} Mbps)")
    print(f"  Ingress per Broker:  {ingress_mb_per_sec/num_brokers:6.1f} MB/s")

if __name__ == "__main__":
    calculate_kafka_capacity()
