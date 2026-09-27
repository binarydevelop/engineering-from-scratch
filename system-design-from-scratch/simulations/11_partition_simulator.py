from typing import Set

class PartitionCluster:
    def __init__(self, total_nodes: int = 5):
        self.total_nodes = total_nodes
        self.majority_quorum = (total_nodes // 2) + 1

    def can_accept_write(self, reachable_nodes: Set[int]) -> bool:
        # Quorum consistency: can only accept writes on the side of the partition with > 50%
        return len(reachable_nodes) >= self.majority_quorum
