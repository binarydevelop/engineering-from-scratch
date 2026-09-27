from typing import Dict, Any, List, Optional

class Node:
    def __init__(self, name: str):
        self.name = name
        self.alive = True
        self.data: Dict[str, Any] = {}

class TinyKVCluster:
    def __init__(self):
        self.nodes = [Node("n1"), Node("n2"), Node("n3")]
        self.hinted_handoff: Dict[str, List[tuple]] = {"n1": [], "n2": [], "n3": []}

    def write_quorum(self, key: str, val: Any, w: int = 2) -> bool:
        acks = 0
        for node in self.nodes:
            if node.alive:
                node.data[key] = val
                acks += 1
            else:
                self.hinted_handoff[node.name].append((key, val))
        return acks >= w

    def read_quorum(self, key: str, r: int = 2) -> Optional[Any]:
        results = []
        for node in self.nodes:
            if node.alive and key in node.data:
                results.append(node.data[key])
        if len(results) >= r:
            return results[0]
        return None
