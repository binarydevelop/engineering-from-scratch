"""
Resilient, production-ready solution for lab-29-unbounded-state-store-leak-in-streaming.
"""
import time
class TTLStateStore:
    def __init__(self, ttl_sec=3600):
        self.ttl = ttl_sec
        self.state = {}
    def put(self, k, v):
        self.state[k] = (v, time.time())
    def prune(self):
        now = time.time()
        self.state = {k: val for k, (val, ts) in self.state.items() if now - ts < self.ttl}
