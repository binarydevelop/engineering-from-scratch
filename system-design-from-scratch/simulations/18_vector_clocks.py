from typing import Dict, Any

class VectorClock:
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.clock: Dict[str, int] = {node_id: 0}

    def increment(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def update(self, other_clock: Dict[str, int]):
        for node, time in other_clock.items():
            self.clock[node] = max(self.clock.get(node, 0), time)
        self.increment()
