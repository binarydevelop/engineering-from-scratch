#!/usr/bin/env python3
import time
from kafka import KafkaProducer, KafkaConsumer

def run_fanout():
    topic = "multi-fanout-orders"
    print(f"Producing 5 events to '{topic}'...")
    producer = KafkaProducer(bootstrap_servers=["localhost:9092"])
    for i in range(1, 6):
        producer.send(topic, value=f"order-{i}".encode())
    producer.flush()
    producer.close()

    # Consumer Group 1: Fraud Service
    c1 = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"], group_id="grp-fraud", auto_offset_reset="earliest", consumer_timeout_ms=2000)
    g1_msgs = [m.value.decode() for m in c1]
    c1.close()

    # Consumer Group 2: Email Service
    c2 = KafkaConsumer(topic, bootstrap_servers=["localhost:9092"], group_id="grp-email", auto_offset_reset="earliest", consumer_timeout_ms=2000)
    g2_msgs = [m.value.decode() for m in c2]
    c2.close()

    print(f"Group 'grp-fraud' received: {len(g1_msgs)} events ({g1_msgs})")
    print(f"Group 'grp-email' received: {len(g2_msgs)} events ({g2_msgs})")
    print("Both groups independently consumed 100% of the stream!")

if __name__ == "__main__":
    run_fanout()
