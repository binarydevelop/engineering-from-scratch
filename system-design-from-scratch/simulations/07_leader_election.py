from typing import List, Dict, Optional

class BullyElectionCluster:
    def __init__(self, node_ids: List[int]):
        self.node_ids = sorted(node_ids)
        self.alive = {nid: True for nid in self.node_ids}
        self.current_leader: Optional[int] = max(self.node_ids)

    def crash_node(self, node_id: int):
        self.alive[node_id] = False
        if self.current_leader == node_id:
            self.current_leader = None

    def elect_leader(self) -> Optional[int]:
        active = [nid for nid in self.node_ids if self.alive[nid]]
        if not active:
            self.current_leader = None
            return None
        self.current_leader = max(active)  # Highest active ID becomes leader
        return self.current_leader
