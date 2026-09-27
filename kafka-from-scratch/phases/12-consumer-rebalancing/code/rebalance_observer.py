#!/usr/bin/env python3
import time
import sys
from kafka import KafkaConsumer, ConsumerRebalanceListener

class LoggingRebalanceListener(ConsumerRebalanceListener):
    def on_partitions_revoked(self, revoked):
        parts = [p.partition for p in revoked]
        print(f" [REBALANCE EVENT] Partitions REVOKED: {parts} (Commit offsets now!)")

    def on_partitions_assigned(self, assigned):
        parts = [p.partition for p in assigned]
        print(f" [REBALANCE EVENT] Partitions ASSIGNED: {parts} (Start fetching!)")

def run_observer(member_name="Consumer-1"):
    print(f"Starting {member_name} with RebalanceListener...")
    consumer = KafkaConsumer(
        "lab-orders",
        bootstrap_servers=["localhost:9092"],
        group_id="rebalance-lab-group",
        enable_auto_commit=True,
        consumer_timeout_ms=10000
    )
    consumer.subscribe(["lab-orders"], listener=LoggingRebalanceListener())

    print(f"{member_name} subscribed. Polling loop active. (Press Ctrl+C to stop)...")
    try:
        while True:
            msg_batch = consumer.poll(timeout_ms=1000)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{member_name} leaving group gracefully...")
    finally:
        consumer.close()
        print(f"{member_name} closed.")

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "Consumer-1"
    run_observer(name)
