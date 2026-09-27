#!/usr/bin/env python3
import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class TopicLogManager:
    def __init__(self, base_dir="/tmp/topics_lab"):
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.topics = {}

    def _get_log(self, topic: str) -> MiniLog:
        if topic not in self.topics:
            topic_file = self.base_dir / f"{topic}.dat"
            self.topics[topic] = MiniLog(str(topic_file))
        return self.topics[topic]

    def produce(self, topic: str, record: bytes) -> int:
        log = self._get_log(topic)
        return log.append(record)

    def consume(self, topic: str, start_offset: int = 0):
        log = self._get_log(topic)
        return log.read_from(start_offset)

    def list_topics(self):
        return [f.stem for f in self.base_dir.glob("*.dat")]

if __name__ == "__main__":
    import shutil
    if os.path.exists("/tmp/topics_lab"):
        shutil.rmtree("/tmp/topics_lab")

    mgr = TopicLogManager()
    print("Producing to independent topics...")
    mgr.produce("orders", b"order-created:1001")
    mgr.produce("orders", b"order-created:1002")
    mgr.produce("payments", b"payment-auth:1001")
    mgr.produce("notifications", b"sms:welcome")

    print(f"\nDiscovered Topics: {mgr.list_topics()}")

    print("\nConsuming 'orders' topic:")
    for off, data in mgr.consume("orders", 0):
        print(f"  [orders] Offset {off}: {data.decode()}")

    print("\nConsuming 'payments' topic:")
    for off, data in mgr.consume("payments", 0):
        print(f"  [payments] Offset {off}: {data.decode()}")
