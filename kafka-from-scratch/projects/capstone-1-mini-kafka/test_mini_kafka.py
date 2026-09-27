#!/usr/bin/env python3
import unittest
import shutil
import os
from pathlib import Path
from mini_kafka import MiniKafkaBroker

class TestMiniKafka(unittest.TestCase):
    STORAGE = "/tmp/test_mini_kafka_unittest"

    def setUp(self):
        if os.path.exists(self.STORAGE):
            shutil.rmtree(self.STORAGE)
        self.broker = MiniKafkaBroker(self.STORAGE)

    def tearDown(self):
        self.broker.close()
        if os.path.exists(self.STORAGE):
            shutil.rmtree(self.STORAGE)

    def test_topic_creation_and_partitioning(self):
        self.broker.create_topic("orders", partitions=3)
        self.assertIn("orders", self.broker.topics)
        self.assertEqual(len(self.broker.topics["orders"]), 3)

    def test_key_hashing_consistency(self):
        self.broker.create_topic("users", partitions=4)
        part1, off1 = self.broker.produce("users", b"user-42", b"data-1")
        part2, off2 = self.broker.produce("users", b"user-42", b"data-2")
        self.assertEqual(part1, part2)
        self.assertEqual(off1, 0)
        self.assertEqual(off2, 1)

    def test_offset_sequentiality_and_fetch(self):
        self.broker.create_topic("payments", partitions=1)
        self.broker.produce("payments", None, b"pay-1")
        self.broker.produce("payments", None, b"pay-2")
        self.broker.produce("payments", None, b"pay-3")

        records = self.broker.fetch("payments", partition=0, start_offset=1)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0][0], 1)
        self.assertEqual(records[0][1], b"pay-2")
        self.assertEqual(records[1][0], 2)
        self.assertEqual(records[1][1], b"pay-3")

    def test_consumer_offset_commits(self):
        self.broker.create_topic("events", partitions=2)
        self.broker.commit_offset("group-a", "events", 0, 42)
        self.assertEqual(self.broker.get_committed_offset("group-a", "events", 0), 42)
        self.assertEqual(self.broker.get_committed_offset("group-b", "events", 0), 0)

    def test_crash_recovery_and_persistence(self):
        self.broker.create_topic("durable", partitions=1)
        self.broker.produce("durable", None, b"durable-event-0")
        self.broker.produce("durable", None, b"durable-event-1")
        self.broker.close()

        # Simulate restart
        new_broker = MiniKafkaBroker(self.STORAGE)
        records = new_broker.fetch("durable", partition=0, start_offset=0)
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1][1], b"durable-event-1")
        # Ensure next append gets offset 2
        part, next_off = new_broker.produce("durable", None, b"durable-event-2")
        self.assertEqual(next_off, 2)
        new_broker.close()

if __name__ == "__main__":
    unittest.main()
