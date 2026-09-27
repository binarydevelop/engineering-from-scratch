#!/usr/bin/env python3
import hashlib

class ShardedIndexSim:
    def __init__(self, num_shards=3):
        self.num_shards = num_shards
        # Each shard is an independent inverted index
        self.shards = {i: {} for i in range(num_shards)}

    def route(self, doc_id):
        # Deterministic hash routing formula
        h = int(hashlib.md5(str(doc_id).encode()).hexdigest(), 16)
        return h % self.num_shards

    def index(self, doc_id, text):
        target_shard = self.route(doc_id)
        self.shards[target_shard][doc_id] = text
        return target_shard

if __name__ == "__main__":
    cluster = ShardedIndexSim(num_shards=3)
    docs = [("item_1", "wireless mouse"), ("item_2", "gaming keyboard"), ("item_3", "hdmi cable"), ("item_4", "desk mat")]
    print("Indexing documents into 3 shards:")
    for d_id, text in docs:
        shard_id = cluster.index(d_id, text)
        print(f"  Doc '{d_id}' -> Assigned to Shard [{shard_id}]")

    print("\nShard Contents:")
    for s_id, s_docs in cluster.shards.items():
        print(f"  Shard {s_id}: {list(s_docs.keys())}")
