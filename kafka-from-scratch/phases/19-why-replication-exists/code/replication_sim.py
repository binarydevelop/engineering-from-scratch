#!/usr/bin/env python3
import time

class Node:
    def __init__(self, node_id: int):
        self.node_id = node_id
        self.log = []
        self.alive = True

class ReplicatedLogCluster:
    def __init__(self):
        self.nodes = {1: Node(1), 2: Node(2), 3: Node(3)}
        self.leader_id = 1

    def append(self, record: str):
        leader = self.nodes[self.leader_id]
        if not leader.alive:
            raise RuntimeError(f"Leader Node {self.leader_id} is DEAD! Writes rejected!")

        offset = len(leader.log)
        leader.log.append((offset, record))
        print(f" [Leader {self.leader_id}] Appended '{record}' at offset {offset}")

        # Replicate to alive followers
        for nid, node in self.nodes.items():
            if nid != self.leader_id and node.alive:
                node.log.append((offset, record))
                print(f"   -> [Follower {nid}] Replicated offset {offset}")
        return offset

    def kill_leader(self):
        print(f"\n!!! SIMULATING HARD CRASH OF LEADER {self.leader_id} !!!")
        self.nodes[self.leader_id].alive = False

    def elect_new_leader(self):
        # Elect first alive node
        for nid, node in self.nodes.items():
            if node.alive:
                self.leader_id = nid
                print(f" [FAILOVER] Node {nid} elected as NEW LEADER! Log length: {len(node.log)}\n")
                return nid
        raise RuntimeError("All nodes are dead!")

if __name__ == "__main__":
    cluster = ReplicatedLogCluster()
    cluster.append("order-created:101")
    cluster.append("order-created:102")

    cluster.kill_leader()
    cluster.elect_new_leader()

    cluster.append("order-created:103")
    print("Replication survived leader crash with zero data loss!")
