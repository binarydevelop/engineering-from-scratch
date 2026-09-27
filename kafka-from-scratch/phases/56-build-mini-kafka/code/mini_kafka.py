#!/usr/bin/env python3
import os
import struct
import zlib
import shutil
from pathlib import Path
from collections import defaultdict

class MiniPartition:
    """An append-only partition log on disk."""
    HEADER_FORMAT = ">QI" # 8-byte uint64 offset, 4-byte uint32 length
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, log_path: str):
        self.log_path = log_path
        self.file = open(log_path, "a+b")
        self.next_offset = self._recover_next_offset()

    def _recover_next_offset(self) -> int:
        self.file.seek(0, os.SEEK_END)
        if self.file.tell() == 0: return 0
        self.file.seek(0, os.SEEK_SET)
        last_offset = -1
        while True:
            hdr = self.file.read(self.HEADER_SIZE)
            if len(hdr) < self.HEADER_SIZE: break
            off, length = struct.unpack(self.HEADER_FORMAT, hdr)
            last_offset = off
            self.file.seek(length, os.SEEK_CUR)
        return last_offset + 1

    def append(self, payload: bytes) -> int:
        off = self.next_offset
        hdr = struct.pack(self.HEADER_FORMAT, off, len(payload))
        self.file.seek(0, os.SEEK_END)
        self.file.write(hdr + payload)
        self.file.flush()
        self.next_offset += 1
        return off

    def read_from(self, start_offset: int):
        self.file.seek(0, os.SEEK_SET)
        records = []
        while True:
            hdr = self.file.read(self.HEADER_SIZE)
            if len(hdr) < self.HEADER_SIZE: break
            off, length = struct.unpack(self.HEADER_FORMAT, hdr)
            payload = self.file.read(length)
            if off >= start_offset:
                records.append((off, payload))
        return records

    def close(self): self.file.close()

class MiniKafkaBroker:
    """A complete single-node Kafka-like engine in Python."""
    def __init__(self, data_dir="/tmp/mini_kafka_storage"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.topics = {} # topic_name -> list[MiniPartition]
        self.consumer_offsets = defaultdict(dict) # group -> { (topic, partition): offset }

    def create_topic(self, topic: str, partitions: int = 3):
        topic_dir = self.data_dir / topic
        topic_dir.mkdir(parents=True, exist_ok=True)
        self.topics[topic] = [
            MiniPartition(str(topic_dir / f"partition-{p}.log"))
            for p in range(partitions)
        ]
        print(f" [Broker] Created topic '{topic}' with {partitions} partitions.")

    def produce(self, topic: str, key: bytes, value: bytes) -> tuple[int, int]:
        if topic not in self.topics:
            self.create_topic(topic, partitions=3)
        parts = self.topics[topic]
        # Hash partitioner
        if key:
            target_partition = (zlib.crc32(key) & 0x7fffffff) % len(parts)
        else:
            target_partition = 0
        offset = parts[target_partition].append(value)
        return target_partition, offset

    def commit_offset(self, group: str, topic: str, partition: int, offset: int):
        self.consumer_offsets[group][(topic, partition)] = offset

    def get_committed_offset(self, group: str, topic: str, partition: int) -> int:
        return self.consumer_offsets[group].get((topic, partition), 0)

    def fetch(self, topic: str, partition: int, start_offset: int):
        return self.topics[topic][partition].read_from(start_offset)

    def close(self):
        for parts in self.topics.values():
            for p in parts: p.close()

if __name__ == "__main__":
    if os.path.exists("/tmp/mini_kafka_storage"):
        shutil.rmtree("/tmp/mini_kafka_storage")

    broker = MiniKafkaBroker()
    broker.create_topic("orders", partitions=2)

    print("\n1. Producing keyed records to MiniKafka:")
    for i in range(1, 5):
        key = f"cust-{i}".encode()
        val = f"order-data-{i}".encode()
        part, off = broker.produce("orders", key, val)
        print(f"  Sent '{val.decode()}' (Key: {key.decode()}) -> Partition {part}, Offset {off}")

    print("\n2. Consuming as Consumer Group 'fulfillment-service':")
    # Worker 1 reads Partition 0
    p0_records = broker.fetch("orders", partition=0, start_offset=0)
    for off, val in p0_records:
        print(f"  [Worker 1] Partition 0 | Offset {off}: {val.decode()}")
        broker.commit_offset("fulfillment-service", "orders", 0, off + 1)

    # Worker 2 reads Partition 1
    p1_records = broker.fetch("orders", partition=1, start_offset=0)
    for off, val in p1_records:
        print(f"  [Worker 2] Partition 1 | Offset {off}: {val.decode()}")
        broker.commit_offset("fulfillment-service", "orders", 1, off + 1)

    print("\n3. Committed Offsets for 'fulfillment-service':")
    for (t, p), off in broker.consumer_offsets["fulfillment-service"].items():
        print(f"  Topic '{t}', Partition {p} -> Committed Offset: {off}")

    broker.close()
    print("\nMiniKafka Capstone 1 executed successfully!")
