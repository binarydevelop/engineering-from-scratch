#!/usr/bin/env python3
"""
bin_packing_sim.py - Capacity Planning & Bin Packing Simulator

Simulates scheduling 100 workloads across two architectural paradigms:
  Strategy A: Many Small Nodes (e.g. 4 CPU, 8 GiB)
  Strategy B: Few Large Nodes   (e.g. 32 CPU, 64 GiB)

Evaluates:
  1. Allocation efficiency and resource fragmentation
  2. Fixed DaemonSet overhead per node (kube-proxy, logging, monitoring)
  3. Blast radius when a single node experiences catastrophic hardware failure
"""

from dataclasses import dataclass
from typing import List

@dataclass
class Workload:
    id: int
    cpu_req: float = 0.5   # 500m
    mem_req: float = 0.5   # 512Mi (0.5 GiB)

@dataclass
class NodeSpec:
    name: str
    cpu_capacity: float
    mem_capacity: float
    # System reserved + DaemonSet fixed overhead per node
    daemon_overhead_cpu: float = 0.4
    daemon_overhead_mem: float = 0.8

def simulate(strategy_name: str, node_cpu: float, node_mem: float, total_pods: int = 100):
    spec = NodeSpec(name=strategy_name, cpu_capacity=node_cpu, mem_capacity=node_mem)
    allocatable_cpu = spec.cpu_capacity - spec.daemon_overhead_cpu
    allocatable_mem = spec.mem_capacity - spec.daemon_overhead_mem

    pod_sample = Workload(id=0)
    pods_per_node_by_cpu = int(allocatable_cpu // pod_sample.cpu_req)
    pods_per_node_by_mem = int(allocatable_mem // pod_sample.mem_req)
    pods_per_node = min(pods_per_node_by_cpu, pods_per_node_by_mem)

    import math
    nodes_needed = math.ceil(total_pods / pods_per_node)
    total_cpu_provisioned = nodes_needed * node_cpu
    total_mem_provisioned = nodes_needed * node_mem

    total_cpu_demanded = total_pods * pod_sample.cpu_req
    total_mem_demanded = total_pods * pod_sample.mem_req

    total_daemon_cpu = nodes_needed * spec.daemon_overhead_cpu
    total_daemon_mem = nodes_needed * spec.daemon_overhead_mem

    cpu_efficiency = (total_cpu_demanded / total_cpu_provisioned) * 100
    mem_efficiency = (total_mem_demanded / total_mem_provisioned) * 100

    # Blast radius: If 1 node dies
    pods_lost_on_node_death = pods_per_node
    pct_outage_on_node_death = (pods_lost_on_node_death / total_pods) * 100

    print(f"============================================================")
    print(f"  Strategy: {strategy_name}")
    print(f"  Node Size: {node_cpu} CPU, {node_mem} GiB RAM")
    print(f"------------------------------------------------------------")
    print(f"  Nodes Required           : {nodes_needed}")
    print(f"  Pods Per Node Capacity   : {pods_per_node}")
    print(f"  Total CPU Provisioned    : {total_cpu_provisioned:.1f} cores (Workload: {total_cpu_demanded:.1f}, Daemon: {total_daemon_cpu:.1f})")
    print(f"  Total RAM Provisioned    : {total_mem_provisioned:.1f} GiB (Workload: {total_mem_demanded:.1f}, Daemon: {total_daemon_mem:.1f})")
    print(f"  CPU Utilization / Eff.   : {cpu_efficiency:.1f}%")
    print(f"  RAM Utilization / Eff.   : {mem_efficiency:.1f}%")
    print(f"  💥 BLAST RADIUS (1 Dead Node):")
    print(f"     Pods Lost Instantly   : {pods_lost_on_node_death} / {total_pods}")
    print(f"     Immediate Capacity Drop: {pct_outage_on_node_death:.1f}% of cluster traffic")
    print(f"============================================================\n")

if __name__ == "__main__":
    print("CAPACITY PLANNING: 100 Microservice Pods (500m CPU, 512Mi RAM each)\n")
    simulate("Strategy A: Many Small Nodes (4 CPU / 8 GiB)", node_cpu=4.0, node_mem=8.0)
    simulate("Strategy B: Few Large Nodes (32 CPU / 64 GiB)", node_cpu=32.0, node_mem=64.0)
