#!/usr/bin/env python3
import time
from kafka import KafkaConsumer, TopicPartition

def check_consumer_lag(topic="lab-orders", group_id="manual-commit-group"):
    print(f"Calculating Consumer Lag for group '{group_id}' on topic '{topic}'...")
    consumer = KafkaConsumer(
        bootstrap_servers=["localhost:9092"],
        group_id=group_id,
        enable_auto_commit=False
    )
    
    # Get partitions for topic
    partitions = consumer.partitions_for_topic(topic)
    if not partitions:
        print(f"Topic '{topic}' has no partitions or does not exist.")
        consumer.close()
        return

    tps = [TopicPartition(topic, p) for p in partitions]
    
    # Query Log End Offsets (broker tail)
    end_offsets = consumer.end_offsets(tps)
    
    total_lag = 0
    print(f"\n{'Partition':<12} {'LEO':<12} {'Committed':<12} {'Lag':<12}")
    print("-" * 48)
    for tp in tps:
        leo = end_offsets.get(tp, 0)
        committed = consumer.committed(tp)
        committed_offset = committed if committed is not None else 0
        lag = max(0, leo - committed_offset)
        total_lag += lag
        print(f"{tp.partition:<12} {leo:<12} {committed_offset:<12} {lag:<12}")

    print("-" * 48)
    print(f"Total Topic Lag: {total_lag} records")
    consumer.close()

if __name__ == "__main__":
    check_consumer_lag()
