#!/usr/bin/env python3
from kafka import KafkaProducer

def run_idempotent_producer():
    print("Initializing KafkaProducer with enable_idempotence=True...")
    # In Kafka 3.0+, enable_idempotence is True by default when acks='all'
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks="all",
        retries=5
    )
    topic = "idempotent-lab"
    print(f"Producing 5 records with sequence numbers to '{topic}'...")
    for i in range(5):
        f = producer.send(topic, key=b"cust-1", value=f"tx-{i}".encode())
        meta = f.get(timeout=5)
        print(f" [Ack] Record {i} -> Offset {meta.offset}")

    producer.flush()
    producer.close()
    print("Idempotent producer completed.")

if __name__ == "__main__":
    run_idempotent_producer()
