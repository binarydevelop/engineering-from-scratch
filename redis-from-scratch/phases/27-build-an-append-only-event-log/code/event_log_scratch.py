#!/usr/bin/env python3
class SimpleEventLog:
    def __init__(self):
        self.entries = [] # [(id, payload)]
        self.next_id = 0

    def append(self, payload):
        entry_id = self.next_id
        self.entries.append((entry_id, payload))
        self.next_id += 1
        return entry_id

    def read_from(self, last_id, count=10):
        return [e for e in self.entries if e[0] > last_id][:count]

if __name__ == "__main__":
    log = SimpleEventLog()
    log.append({"event": "user_signup", "uid": 1})
    log.append({"event": "order_created", "order_id": 99})
    log.append({"event": "payment_received", "amount": 50})

    print("Worker Alpha consuming from beginning:")
    worker_alpha_offset = -1
    msgs = log.read_from(worker_alpha_offset)
    for mid, payload in msgs:
        print(f"  Worker Alpha read: ID {mid} -> {payload}")
        worker_alpha_offset = mid

    print("\nWorker Beta consuming later:")
    worker_beta_offset = 0 # Missed first event
    msgs = log.read_from(worker_beta_offset)
    for mid, payload in msgs:
        print(f"  Worker Beta read: ID {mid} -> {payload}")
