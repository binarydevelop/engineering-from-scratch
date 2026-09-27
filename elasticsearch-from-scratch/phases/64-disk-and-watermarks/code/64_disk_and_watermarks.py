#!/usr/bin/env python3

def evaluate_disk_status(disk_pct):
    if disk_pct >= 95:
        return "FLOOD_STAGE", "Action: Index locked READ-ONLY (index.blocks.read_only_allow_delete: true). All writes rejected."
    elif disk_pct >= 90:
        return "HIGH_WATERMARK", "Action: Master attempts to relocate existing shards away from this node."
    elif disk_pct >= 85:
        return "LOW_WATERMARK", "Action: Master stops allocating new shards to this node."
    return "HEALTHY", "Normal operations."

if __name__ == "__main__":
    for usage in [75, 87, 92, 97]:
        stage, action = evaluate_disk_status(usage)
        print(f"Disk at {usage}% -> [{stage:15s}] : {action}")
