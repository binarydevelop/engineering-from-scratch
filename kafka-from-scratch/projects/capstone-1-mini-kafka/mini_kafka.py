#!/usr/bin/env python3
"""
Capstone 1: Mini-Kafka Engine
A self-contained, educational distributed log broker in pure Python.
Demonstrates:
  - Topics and Partitions
  - Length-prefixed append-only disk logs
  - Monotonic 64-bit partition offsets
  - Hash-based key partitioning
  - Consumer group partition assignment and offset commits
  - Crash recovery and persistence across restarts
"""

import os
import struct
import zlib
from pathlib import Path
from collections import defaultdict
from typing import List, Tuple, Dict, Optional

class PartitionLog:
    """An immutable, append-only disk log for a single topic-partition."""
    HEADER_FORMAT = ">QI" # 8-byte uint64 monotonic offset, 4-byte uint32 payload length
    HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

    def __init__(self, log_path: str):
        self.log_path = log_path
        self.file = open(log_path, "a+b")
        self.next_offset = self._recover_next_offset()

    def _recover_next_offset(self) -> int:
        self.file.seek(0, os.SEEK_END)
        size = self.file.tell()
        if size == 0:
            return 0
        self.file.seek(0, os.SEEK_SET)
        last_offset = -1
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            last_offset = offset
            self.file.seek(length, os.SEEK_CUR) # Skip payload bytes
        return last_offset + 1

    def append(self, payload: bytes) -> int:
        offset = self.next_offset
        header = struct.pack(self.HEADER_FORMAT, offset, len(payload))
        self.file.seek(0, os.SEEK_END)
        self.file.write(header + payload)
        self.file.flush()
        self.next_offset += 1
        return offset

    def read_from(self, start_offset: int) -> List[Tuple[int, bytes]]:
        self.file.seek(0, os.SEEK_SET)
        records = []
        while True:
            header_bytes = self.file.read(self.HEADER_SIZE)
            if len(header_bytes) < self.HEADER_SIZE:
                break
            offset, length = struct.unpack(self.HEADER_FORMAT, header_bytes)
            payload = self.file.read(length)
            if offset >= start_offset:
                records.append((offset, payload))
        return records

    def close(self):
        self.file.close()

class MiniKafkaBroker:
    """The central broker managing topics, partitions, and consumer groups."""
    def __init__(self, storage_dir: str = "/tmp/mini_kafka_broker_data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.topics: Dict[str, List[PartitionLog]] = {}
        self.consumer_offsets: Dict[str, Dict[Tuple[str, int], int]] = defaultdict(dict)
        self._load_existing_topics()

    def _load_existing_topics(self):
        for topic_dir in self.storage_dir.iterdir():
            if topic_dir.is_dir():
                topic_name = topic_dir.name
                log_files = sorted(list(topic_dir.glob("partition-*.log")))
                self.topics[topic_name] = [PartitionLog(str(f)) for f in log_files]

    def create_topic(self, topic: str, partitions: int = 3):
        if topic in self.topics:
            return
        topic_dir = self.storage_dir / topic
        topic_dir.mkdir(parents=True, exist_ok=True)
        self.topics[topic] = [
            PartitionLog(str(topic_dir / f"partition-{p}.log"))
            for p in range(partitions)
        ]

    def produce(self, topic: str, key: Optional[bytes], value: bytes) -> Tuple[int, int]:
        if topic not in self.topics:
            self.create_topic(topic, partitions=3)
        parts = self.topics[topic]
        if key:
            target_partition = (zlib.crc32(key) & 0x7fffffff) % len(parts)
        else:
            target_partition = 0
        offset = parts[target_partition].append(value)
        return target_partition, offset

    def fetch(self, topic: str, partition: int, start_offset: int) -> List[Tuple[int, bytes]]:
        if topic not in self.topics or partition >= len(self.topics[topic]):
            return []
        return self.topics[topic][partition].read_from(start_offset)

    def commit_offset(self, group: str, topic: str, partition: int, offset: int):
        self.consumer_offsets[group][(topic, partition)] = offset

    def get_committed_offset(self, group: str, topic: str, partition: int) -> int:
        return self.consumer_offsets[group].get((topic, partition), 0)

    def close(self):
        for parts in self.topics.values():
            for p in parts:
                p.close()
