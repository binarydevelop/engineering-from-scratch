"""
Broken implementation demonstrating the flaw in lab-29-unbounded-state-store-leak-in-streaming.
"""
class UnboundedState:
    def __init__(self):
        self.state = {}
    def put(self, k, v):
        self.state[k] = v # Never evicts -> OOM
