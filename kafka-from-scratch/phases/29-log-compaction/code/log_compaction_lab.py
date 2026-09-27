#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def test_compaction():
    topic = "compacted-users"
    print(f"Producing state updates to compacted topic '{topic}'...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        key_serializer=lambda k: k.encode("utf-8"),
        value_serializer=lambda v: v.encode("utf-8") if v is not None else None
    )

    # User 1 updates
    producer.send(topic, key="user-1", value="Alice v1 (Seattle)")
    producer.send(topic, key="user-2", value="Bob v1 (New York)")
    producer.send(topic, key="user-1", value="Alice v2 (Chicago)")
    producer.send(topic, key="user-1", value="Alice v3 (London)")
    
    # Tombstone for User 2 (delete marker)
    producer.send(topic, key="user-2", value=None)

    producer.flush()
    producer.close()
    print("Produced state updates + tombstone.")

if __name__ == "__main__":
    test_compaction()
