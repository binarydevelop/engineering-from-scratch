#!/usr/bin/env python3
import os
import sys
import shutil
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../02-build-an-append-only-log/code")))
from mini_log import MiniLog

class PartitionedLog:
    def __init__(self, topic_dir="/tmp/partitioned_topic", num_partitions=3):
        self.topic_dir = Path(topic_dir)
        self.topic_dir.mkdir(parents=True, exist_ok=True)
        self.num_partitions = num_partitions
        self.partitions = [
            MiniLog(str(self.topic_dir / f"partition-{p}.dat"))
            for p in range(num_partitions)
        ]
        self.round_robin_counter = 0

    def append(self, payload: bytes) -> tuple[int, int]:
        target_partition = self.round_robin_counter % self.num_partitions
        self.round_robin_counter += 1
        offset = self.partitions[target_partition].append(payload)
        return target_partition, offset

    def close(self):
        for p in self.partitions:
            p.close()

if __name__ == "__main__":
    if os.path.exists("/tmp/partitioned_topic"):
        shutil.rmtree("/tmp/partitioned_topic")

    plog = PartitionedLog(num_partitions=3)
    print("Appending 9 records across 3 partitions (Round-Robin):\n")
    for i in range(9):
        msg = f"event-{i}".encode()
        partition, offset = plog.append(msg)
        print(f" Message '{msg.decode()}' -> Landed in Partition {partition} at Offset {offset}")

    plog.close()
    print("\nNotice: Each partition maintains its own local offsets (0, 1, 2)!")
