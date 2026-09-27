#!/usr/bin/env python3
"""
Unit tests for Distributed Cluster Simulator (Phase 81).
"""

import unittest
from cluster_simulator import ShardNode, CoordinatingNode

class TestDistributedCluster(unittest.TestCase):
    def setUp(self):
        self.nodes = [ShardNode(0), ShardNode(1), ShardNode(2)]
        self.cluster = CoordinatingNode(self.nodes)
        for i in range(15):
            self.cluster.index(i, {"text": f"distributed search item {i}"})

    def test_scatter_gather(self):
        res = self.cluster.search("distributed", top_k=5)
        self.assertEqual(res["_shards"]["total"], 3)
        self.assertEqual(res["_shards"]["successful"], 3)
        self.assertEqual(len(res["hits"]), 5)

    def test_failed_shard_partial_hits(self):
        # Kill shard 1
        self.nodes[1].is_alive = False
        res = self.cluster.search("distributed", top_k=5)
        self.assertEqual(res["_shards"]["successful"], 2)
        self.assertEqual(res["_shards"]["failed"], 1)
        self.assertTrue(len(res["hits"]) > 0) # Still returns partial hits!

if __name__ == "__main__":
    unittest.main()
