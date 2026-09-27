import hashlib
import bisect
from typing import Dict, List, Optional, Any

class DistributedCacheCluster:
    def __init__(self, virtual_nodes: int = 40):
        self.virtual_nodes = virtual_nodes
        self.ring: List[int] = []
        self.ring_map: Dict[int, str] = {}
        self.storage: Dict[str, Dict[str, Any]] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node_id: str):
        self.storage[node_id] = {}
        for i in range(self.virtual_nodes):
            h = self._hash(f"{node_id}#vn_{i}")
            self.ring_map[h] = node_id
            bisect.insort(self.ring, h)

    def remove_node(self, node_id: str):
        if node_id in self.storage:
            del self.storage[node_id]
        to_del = [h for h, n in self.ring_map.items() if n == node_id]
        for h in to_del:
            del self.ring_map[h]
            self.ring.remove(h)

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.ring_map[self.ring[idx]]

    def put(self, key: str, val: Any):
        node = self.get_node(key)
        if node:
            self.storage[node][key] = val

    def get(self, key: str) -> Any:
        node = self.get_node(key)
        if node and node in self.storage:
            return self.storage[node].get(key)
        return None
