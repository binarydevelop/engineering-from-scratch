#!/usr/bin/env python3
import hashlib

def get_shard(routing_key, num_shards=5):
    h = int(hashlib.md5(str(routing_key).encode()).hexdigest(), 16)
    return h % num_shards

if __name__ == "__main__":
    num_shards = 5
    tenants = ["acme_corp", "globex", "initech", "umbrella_corp"]
    print(f"Cluster with {num_shards} Primary Shards:\n")
    for t in tenants:
        shard = get_shard(t, num_shards)
        print(f"Tenant '{t:15s}' ──► Routed exclusively to Shard [{shard}]")
    print("\nWhen querying tenant 'acme_corp', the coordinator only queries Shard [", get_shard("acme_corp", num_shards), "]!")
