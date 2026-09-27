#!/usr/bin/env python3

def assess_cluster_metrics(metrics):
    alerts = []
    if metrics["health"] != "green":
        alerts.append(f"CRITICAL: Cluster health is {metrics['health'].upper()}!")
    if metrics["heap_pct"] > 85:
        alerts.append(f"WARNING: High JVM Heap pressure: {metrics['heap_pct']}%")
    if metrics["rejected_writes"] > 0:
        alerts.append(f"CRITICAL: Write thread pool has {metrics['rejected_writes']} rejected tasks!")
    if metrics["disk_usage_pct"] > 85:
        alerts.append(f"WARNING: Disk usage at {metrics['disk_usage_pct']}% (near low watermark)")
    return alerts

if __name__ == "__main__":
    snapshot = {
        "health": "yellow",
        "heap_pct": 88,
        "rejected_writes": 142,
        "disk_usage_pct": 82
    }
    print("Observability Health Assessment:")
    issues = assess_cluster_metrics(snapshot)
    for issue in issues:
        print("  -", issue)
