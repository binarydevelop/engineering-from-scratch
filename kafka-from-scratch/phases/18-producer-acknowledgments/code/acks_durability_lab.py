#!/usr/bin/env python3
import time
from kafka import KafkaProducer

def measure_acks(acks_setting, n=100):
    producer = KafkaProducer(
        bootstrap_servers=["localhost:9092"],
        acks=acks_setting
    )
    topic = f"acks-lab-{acks_setting}"
    start = time.time()
    for i in range(n):
        future = producer.send(topic, value=b"test-payload-durability")
        if acks_setting != 0:
            future.get(timeout=5)
    dur = time.time() - start
    producer.close()
    return (dur / n) * 1000

if __name__ == "__main__":
    print("Measuring Producer Latency by Acks Setting (100 records):\n")
    lat_0 = measure_acks(0)
    print(f" acks=0   (Fire-and-forget) : {lat_0:6.2f} ms/record")

    lat_1 = measure_acks(1)
    print(f" acks=1   (Leader local)    : {lat_1:6.2f} ms/record")

    lat_all = measure_acks("all")
    print(f" acks=all (ISR Quorum)      : {lat_all:6.2f} ms/record")
