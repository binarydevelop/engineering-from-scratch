#!/usr/bin/env python3
import random

class SimulatedBroker:
    def __init__(self):
        self.log = []

    def append(self, record):
        offset = len(self.log)
        self.log.append((offset, record))
        return offset

def produce_with_unreliable_ack(broker, record, drop_ack_probability=0.5):
    print(f"\n[Producer] Sending: '{record}'")
    # 1. Broker receives and writes
    offset = broker.append(record)
    print(f"  -> Broker wrote to disk at Offset {offset}")

    # 2. Network simulation for Ack
    if random.random() < drop_ack_probability:
        print("  -> [NETWORK GLITCH] Ack packet DROPPED in transit!")
        print("  -> [Producer] Timeout! Did not receive Ack. RETRYING...")
        # Retry!
        retry_offset = broker.append(record)
        print(f"  -> Broker accepted RETRY write to disk at Offset {retry_offset}")
        print("  -> Ack received.")
    else:
        print("  -> Ack delivered successfully.")

if __name__ == "__main__":
    broker = SimulatedBroker()
    # Force a dropped ack
    produce_with_unreliable_ack(broker, "payment:ord_101", drop_ack_probability=1.0)

    print("\nFinal Broker Log:")
    for off, msg in broker.log:
        print(f"  Offset {off}: {msg}")
    print("Result: Duplicate records created because producer retried after dropped Ack!")
