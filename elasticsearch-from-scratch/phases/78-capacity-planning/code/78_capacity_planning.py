#!/usr/bin/env python3

def plan_capacity(raw_gb_day, retention_days, replicas=1, overhead_factor=1.2, target_shard_gb=40.0):
    daily_indexed_gb = raw_gb_day * overhead_factor
    daily_total_gb = daily_indexed_gb * (1 + replicas)
    total_data_gb = daily_total_gb * retention_days
    # Add 30% safety margin for watermarks and merge headroom
    recommended_disk_gb = total_data_gb * 1.3
    primary_shards_per_day = max(1, round(daily_indexed_gb / target_shard_gb))

    return {
        "daily_indexed_gb": round(daily_indexed_gb, 1),
        "total_retained_data_tb": round(total_data_gb / 1024, 2),
        "recommended_physical_disk_tb": round(recommended_disk_gb / 1024, 2),
        "primary_shards_per_day": primary_shards_per_day,
        "total_shards_active": primary_shards_per_day * (1 + replicas) * retention_days
    }

if __name__ == "__main__":
    plan = plan_capacity(raw_gb_day=200, retention_days=30, replicas=1)
    print("Capacity Planning Report (200 GB/day, 30 days retention, 1 replica):")
    for k, v in plan.items():
        print(f"  {k:30s}: {v}")
