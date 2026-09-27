#!/usr/bin/env python3
import socket
import threading
import time

class PrimaryReplicaToy:
    def __init__(self):
        self.primary_store = {}
        self.replica_store = {}
        self.repl_backlog = []

    def primary_write(self, key, val):
        self.primary_store[key] = val
        self.repl_backlog.append((key, val))
        print(f"  [Primary] Written {key}={val}. Client acknowledged (+OK).")

    def sync_replica(self, delay_sec=0.2):
        time.sleep(delay_sec) # Simulate network lag
        while self.repl_backlog:
            k, v = self.repl_backlog.pop(0)
            self.replica_store[k] = v
            print(f"  [Replica] Applied replication stream: {k}={v}")

if __name__ == "__main__":
    toy = PrimaryReplicaToy()
    print("1. Writing to Primary:")
    toy.primary_write("user:10", "Alice")
    print(f"  Immediate Replica Read: {toy.replica_store.get('user:10')} (Stale read during replication lag!)")
    
    print("\n2. Replicating over asynchronous network:")
    toy.sync_replica()
    print(f"  Replica Read After Sync: {toy.replica_store.get('user:10')} (Consistent)")
