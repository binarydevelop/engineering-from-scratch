#!/usr/bin/env python3
import json
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata

def run_manual_commit_demo():
    print("Connecting consumer with manual commit (enable_auto_commit=False)...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        group_id="manual-commit-group",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        consumer_timeout_ms=5000
    )

    records = consumer.poll(timeout_ms=2000)
    print(f"Polled {sum(len(v) for v in records.values())} records across {len(records)} partitions.")

    for tp, batch in records.items():
        print(f"\nProcessing partition {tp.partition}:")
        for record in batch:
            print(f"  Processed record offset: {record.offset}")
        
        # Commit exact next offset (offset + 1)
        last_offset = batch[-1].offset
        consumer.commit({
            tp: OffsetAndMetadata(last_offset + 1, "processed-by-worker-1")
        })
        print(f" [COMMITTED] Successfully committed offset {last_offset + 1} for partition {tp.partition}")

    consumer.close()

if __name__ == "__main__":
    run_manual_commit_demo()
