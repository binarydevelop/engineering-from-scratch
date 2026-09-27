#!/usr/bin/env python3
"""
Production Capacity Planning & Headroom Engine.

Models microservice resource consumption, Little's Law concurrency,
database connection demand, and forecasts scaling cliffs.
"""

import math
from typing import Dict, Any


def plan_capacity(
    peak_rps: float,
    avg_latency_ms: float,
    cpu_ms_per_request: float,
    memory_mb_per_replica: float,
    db_queries_per_request: int,
    desired_headroom_percent: float = 40.0,
    core_cpu_capacity_cores: float = 2.0
) -> Dict[str, Any]:
    """
    Computes capacity requirements based on traffic parameters.
    """
    # 1. Little's Law Concurrency: L = lambda * W
    avg_latency_sec = avg_latency_ms / 1000.0
    concurrency_needed = peak_rps * avg_latency_sec

    # 2. CPU Consumption
    # CPU cores = (RPS * CPU_ms_per_req) / 1000ms
    raw_cpu_cores_needed = (peak_rps * cpu_ms_per_request) / 1000.0
    
    # Apply headroom multiplier: E.g., 40% headroom means operating at 60% capacity
    utilization_target = (100.0 - desired_headroom_percent) / 100.0
    total_cpu_cores_with_headroom = raw_cpu_cores_needed / utilization_target

    # Replicas required (assuming core_cpu_capacity_cores per replica)
    replicas_needed = math.ceil(total_cpu_cores_with_headroom / core_cpu_capacity_cores)
    total_memory_gb = (replicas_needed * memory_mb_per_replica) / 1024.0

    # 3. Database Demand
    total_db_qps = peak_rps * db_queries_per_request
    # Recommended connection pool slots: Little's Law applied to DB query latency (~10ms)
    db_concurrency = total_db_qps * 0.010
    recommended_db_pool_per_replica = math.ceil(db_concurrency / replicas_needed * 1.5)

    return {
        "peak_rps": peak_rps,
        "latency_ms": avg_latency_ms,
        "concurrency_needed": concurrency_needed,
        "raw_cpu_cores": raw_cpu_cores_needed,
        "total_cpu_cores_with_headroom": total_cpu_cores_with_headroom,
        "replicas_needed": replicas_needed,
        "total_memory_gb": total_memory_gb,
        "total_db_qps": total_db_qps,
        "recommended_db_pool_per_replica": recommended_db_pool_per_replica,
        "headroom_percent": desired_headroom_percent,
        "target_utilization_percent": utilization_target * 100.0
    }


def main():
    results = plan_capacity(
        peak_rps=2500,
        avg_latency_ms=65,
        cpu_ms_per_request=12.0,
        memory_mb_per_replica=512,
        db_queries_per_request=3,
        desired_headroom_percent=40.0
    )

    print("=========================================================================")
    print("           PRODUCTION CAPACITY SIZING & HEADROOM REPORT                  ")
    print("=========================================================================")
    print(f" Peak Demand:                 {results['peak_rps']:,} RPS @ {results['latency_ms']:.1f}ms latency")
    print(f" Average Concurrency (L):     {results['concurrency_needed']:.1f} concurrent in-flight requests")
    print("-------------------------------------------------------------------------")
    print(f" Raw CPU Required:            {results['raw_cpu_cores']:.2f} cores (100% busy)")
    print(f" Sized CPU (with Headroom):   {results['total_cpu_cores_with_headroom']:.2f} cores (Operating at {results['target_utilization_percent']:.0f}% max)")
    print(f" Minimum Required Replicas:   {results['replicas_needed']} pods (2-core pods)")
    print(f" Total Cluster Memory:        {results['total_memory_gb']:.2f} GB RAM")
    print("-------------------------------------------------------------------------")
    print(f" Database Total Query Rate:   {results['total_db_qps']:,} QPS")
    print(f" Pool Size Per Replica:       {results['recommended_db_pool_per_replica']} connections / pod")
    print("=========================================================================")


if __name__ == "__main__":
    main()
