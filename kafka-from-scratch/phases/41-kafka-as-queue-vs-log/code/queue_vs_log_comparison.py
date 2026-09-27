#!/usr/bin/env python3
from collections import deque

class DestructiveQueue:
    def __init__(self):
        self.queue = deque()
    def push(self, item): self.queue.append(item)
    def pop(self): return self.queue.popleft() if self.queue else None

class NonDestructiveLog:
    def __init__(self):
        self.log = []
    def append(self, item):
        off = len(self.log)
        self.log.append((off, item))
        return off
    def read(self, offset):
        return self.log[offset:]

if __name__ == "__main__":
    print("--- 1. Destructive Queue (Work Queue Model) ---")
    q = DestructiveQueue()
    q.push("Task-1")
    q.push("Task-2")
    print(f" Worker A pops: {q.pop()}")
    print(f" Worker B pops: {q.pop()}")
    print(f" Remaining in queue: {len(q.queue)} (Data is GONE! Cannot replay!)\n")

    print("--- 2. Non-Destructive Log (Kafka Model) ---")
    log = NonDestructiveLog()
    log.append("Event-1")
    log.append("Event-2")
    print(f" Service A (Fraud) reads:     {[x[1] for x in log.read(0)]}")
    print(f" Service B (Analytics) reads: {[x[1] for x in log.read(0)]}")
    print(f" Service C (Replay next day): {[x[1] for x in log.read(0)]}")
    print(" Result: Data remains immutable on disk for all consumers!")
