import hashlib
import bisect
from typing import Dict, List, Optional

class ConsistentHashRing:
    def __init__(self, virtual_nodes: int = 100):
        self.virtual_nodes = virtual_nodes
        self.ring: List[int] = []
        self.ring_map: Dict[int, str] = {}
        self.physical_nodes: set = set()

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str):
        self.physical_nodes.add(node)
        for i in range(self.virtual_nodes):
            v_key = f"{node}#vn_{i}"
            h = self._hash(v_key)
            self.ring_map[h] = node
            bisect.insort(self.ring, h)

    def remove_node(self, node: str):
        if node not in self.physical_nodes:
            return
        self.physical_nodes.remove(node)
        to_remove = [h for h, n in self.ring_map.items() if n == node]
        for h in to_remove:
            del self.ring_map[h]
            self.ring.remove(h)

    def get_node(self, key: str) -> Optional[str]:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0  # Wrap around
        return self.ring_map[self.ring[idx]]
