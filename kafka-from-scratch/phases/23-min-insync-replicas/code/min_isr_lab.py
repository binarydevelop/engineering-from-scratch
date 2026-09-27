#!/usr/bin/env python3
from kafka import KafkaProducer
from kafka.errors import NotEnoughReplicasError, KafkaError

def test_min_isr_write(topic="durable-topic"):
    print(f"Testing produce write with acks='all' to topic '{topic}'...")
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092", "localhost:9094", "localhost:9096"],
        acks="all",
        request_timeout_ms=3000
    )
    try:
        f = producer.send(topic, value=b"critical-financial-event")
        meta = f.get(timeout=4)
        print(f" [SUCCESS] Write accepted! Offset {meta.offset} on partition {meta.partition}")
    except NotEnoughReplicasError:
        print(" [REJECTED] NotEnoughReplicasError: Current ISR size is below min.insync.replicas!")
    except KafkaError as e:
        print(f" [ERROR] Kafka error: {e}")
    finally:
        producer.close()

if __name__ == "__main__":
    test_min_isr_write()
