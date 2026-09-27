#!/usr/bin/env python3
"""
scheduler_sim.py - Scheduling From First Principles

Simulates the core Kubernetes scheduling pipeline:
    1. FILTER (Pre-filter / Predicates): Remove nodes that cannot run the Pod
    2. SCORE (Priorities): Rank surviving nodes based on resource balancing and spreading
    3. BIND: Assign winning node and decrement its allocatable capacity
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

@dataclass
class Taint:
    key: str
    value: str
    effect: str = "NoSchedule"

@dataclass
class Toleration:
    key: str
    value: str
    effect: str = "NoSchedule"

@dataclass
class Node:
    name: str
    cpu_allocatable: float     # In cores (e.g., 4.0)
    memory_allocatable: float  # In MiB (e.g., 8192)
    labels: Dict[str, str] = field(default_factory=dict)
    taints: List[Taint] = field(default_factory=list)
    cpu_used: float = 0.0
    memory_used: float = 0.0
    assigned_pods: List[str] = field(default_factory=list)

    @property
    def free_cpu(self) -> float:
        return self.cpu_allocatable - self.cpu_used

    @property
    def free_memory(self) -> float:
        return self.memory_allocatable - self.memory_used

@dataclass
class Pod:
    name: str
    cpu_request: float
    memory_request: float
    node_selector: Dict[str, str] = field(default_factory=dict)
    tolerations: List[Toleration] = field(default_factory=list)
    bound_node: Optional[str] = None

class SchedulerSimulator:
    def __init__(self, nodes: List[Node]):
        self.nodes = {n.name: n for n in nodes}

    def filter_node(self, pod: Pod, node: Node) -> Tuple[bool, str]:
        """Stage 1: Filter. Checks if the node has sufficient resources and matches constraints."""
        # 1. Check CPU capacity
        if node.free_cpu < pod.cpu_request:
            return False, f"Insufficient CPU (requires {pod.cpu_request}, free {node.free_cpu})"

        # 2. Check Memory capacity
        if node.free_memory < pod.memory_request:
            return False, f"Insufficient Memory (requires {pod.memory_request}Mi, free {node.free_memory}Mi)"

        # 3. Check NodeSelector
        for key, val in pod.node_selector.items():
            if node.labels.get(key) != val:
                return False, f"NodeSelector mismatch ({key}={val} not on node)"

        # 4. Check Taints & Tolerations
        for taint in node.taints:
            if taint.effect == "NoSchedule":
                tolerated = any(
                    tol.key == taint.key and tol.value == taint.value and tol.effect == taint.effect
                    for tol in pod.tolerations
                )
                if not tolerated:
                    return False, f"Untolerated taint ({taint.key}={taint.value}:{taint.effect})"

        return True, "Node fits"

    def score_node(self, pod: Pod, node: Node) -> float:
        """Stage 2: Score. Computes a balanced resource score between 0 and 100."""
        # Simulated NodeResourcesBalancedAllocation algorithm
        cpu_fraction = (node.cpu_used + pod.cpu_request) / node.cpu_allocatable
        mem_fraction = (node.memory_used + pod.memory_request) / node.memory_allocatable
        
        # Balance score: Higher score when CPU and Memory utilization ratios match
        diff = abs(cpu_fraction - mem_fraction)
        balance_score = (1.0 - diff) * 50.0

        # Least allocated score: Prefers spreading pods across empty nodes
        spare_cpu_fraction = (node.free_cpu - pod.cpu_request) / node.cpu_allocatable
        spare_mem_fraction = (node.free_memory - pod.memory_request) / node.memory_allocatable
        least_alloc_score = ((spare_cpu_fraction + spare_mem_fraction) / 2.0) * 50.0

        return balance_score + least_alloc_score

    def schedule_pod(self, pod: Pod) -> Optional[str]:
        print(f"\n[SCHEDULER] Attempting to schedule Pod '{pod.name}' (CPU: {pod.cpu_request}, RAM: {pod.memory_request}Mi)...")
        surviving_nodes: List[Node] = []

        # 1. Filter Phase
        for node in self.nodes.values():
            fits, reason = self.filter_node(pod, node)
            if fits:
                print(f"  [FILTER] Node '{node.name}' PASSED.")
                surviving_nodes.append(node)
            else:
                print(f"  [FILTER] Node '{node.name}' REJECTED: {reason}.")

        if not surviving_nodes:
            print(f"  [FAILED] Pod '{pod.name}' could not be scheduled on any node (Status: Pending)!")
            return None

        # 2. Score Phase
        scores = {}
        for node in surviving_nodes:
            score = self.score_node(pod, node)
            scores[node.name] = score
            print(f"  [SCORE]  Node '{node.name}' Score = {score:.2f}/100")

        # 3. Bind Phase
        winning_node_name = max(scores, key=scores.get)
        winning_node = self.nodes[winning_node_name]
        winning_node.cpu_used += pod.cpu_request
        winning_node.memory_used += pod.memory_request
        winning_node.assigned_pods.append(pod.name)
        pod.bound_node = winning_node_name
        print(f"  [BIND]   Successfully bound '{pod.name}' to Node '{winning_node_name}'.")
        return winning_node_name

def test_scheduler():
    # Build 3 Nodes
    nodes = [
        Node(name="worker-01", cpu_allocatable=4.0, memory_allocatable=8192, labels={"zone": "us-east-1a"}),
        Node(name="worker-02", cpu_allocatable=8.0, memory_allocatable=16384, labels={"zone": "us-east-1b"}),
        Node(name="worker-gpu", cpu_allocatable=8.0, memory_allocatable=32768, 
             labels={"zone": "us-east-1c", "accelerator": "nvidia"},
             taints=[Taint(key="sku", value="gpu", effect="NoSchedule")]),
    ]
    scheduler = SchedulerSimulator(nodes)

    # 1. Schedule normal web app
    pod1 = Pod(name="web-01", cpu_request=1.0, memory_request=1024)
    winner1 = scheduler.schedule_pod(pod1)
    assert winner1 in ["worker-01", "worker-02"]

    # 2. Schedule GPU workload without toleration -> Must reject GPU node
    pod_cpu_heavy = Pod(name="cpu-batch", cpu_request=6.0, memory_request=2048)
    winner2 = scheduler.schedule_pod(pod_cpu_heavy)
    assert winner2 == "worker-02" # Only worker-02 has 6 CPU and no taint

    # 3. Workload with GPU toleration and selector -> Must bind to worker-gpu
    pod_ml = Pod(name="model-train", cpu_request=4.0, memory_request=8192,
                 node_selector={"accelerator": "nvidia"},
                 tolerations=[Toleration(key="sku", value="gpu", effect="NoSchedule")])
    winner3 = scheduler.schedule_pod(pod_ml)
    assert winner3 == "worker-gpu"

    # 4. Workload requesting impossible resources -> Must fail (Pending)
    pod_impossible = Pod(name="monster", cpu_request=32.0, memory_request=65536)
    winner4 = scheduler.schedule_pod(pod_impossible)
    assert winner4 is None

    print("\n[VERIFICATION] All scheduler simulation test cases passed successfully!")

if __name__ == "__main__":
    test_scheduler()
