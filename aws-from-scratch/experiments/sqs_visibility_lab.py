#!/usr/bin/env python3
"""
experiments/sqs_visibility_lab.py
Phases 33, 34 & 35: SQS Visibility Timeout, Worker Failures, & Idempotency

This lab demonstrates the fundamental systems physics of distributed message queues:
  1. At-Least-Once Delivery: Why messages can be delivered more than once.
  2. Visibility Timeout: What happens when a consumer crashes before calling DeleteMessage.
  3. Poison Pill Messages: How repeatedly failing messages cycle through the queue.
  4. Dead-Letter Queue (DLQ): Safely isolating unprocessable messages after maxReceiveCount.
  5. Idempotent Consumer: Ensuring business side effects happen exactly once.
"""

import time
import uuid
from typing import Dict, List, Optional, Set


class SQSMessage:
    def __init__(self, body: str, message_id: Optional[str] = None):
        self.message_id = message_id or str(uuid.uuid4())[:8]
        self.body = body
        self.receive_count = 0
        self.visible_at = 0.0  # Unix timestamp when message becomes visible again


class MockSQSQueue:
    def __init__(self, name: str, visibility_timeout_sec: float = 2.0, max_receive_count: int = 3, dlq: Optional["MockSQSQueue"] = None):
        self.name = name
        self.visibility_timeout_sec = visibility_timeout_sec
        self.max_receive_count = max_receive_count
        self.dlq = dlq
        self.messages: Dict[str, SQSMessage] = {}

    def send_message(self, body: str) -> str:
        msg = SQSMessage(body)
        self.messages[msg.message_id] = msg
        return msg.message_id

    def receive_message(self) -> Optional[SQSMessage]:
        now = time.time()
        for msg_id, msg in list(self.messages.items()):
            if msg.visible_at <= now:
                # Message is visible!
                msg.receive_count += 1
                
                # Check for DLQ transfer
                if self.dlq and msg.receive_count > self.max_receive_count:
                    print(f"  [DLQ ALERT] Message {msg.message_id} exceeded maxReceiveCount ({self.max_receive_count}). Evicting to DLQ: {self.dlq.name}")
                    del self.messages[msg_id]
                    self.dlq.messages[msg_id] = msg
                    msg.visible_at = 0.0
                    return None

                # Hide message for the visibility timeout duration
                msg.visible_at = now + self.visibility_timeout_sec
                return msg
        return None

    def delete_message(self, message_id: str) -> bool:
        if message_id in self.messages:
            del self.messages[message_id]
            return True
        return False

    def approximate_number_of_messages(self) -> int:
        now = time.time()
        return sum(1 for m in self.messages.values() if m.visible_at <= now)


class IdempotentPaymentConsumer:
    """
    Consumer that processes payments idempotently using a deduplication cache.
    Delivery is at-least-once, but business side-effect is exactly-once.
    """
    def __init__(self):
        self.processed_order_ids: Set[str] = set()
        self.processed_bank_charges: List[Dict[str, Any]] = []

    def process_message(self, msg: SQSMessage, should_crash: bool = False) -> bool:
        order_id = msg.body
        print(f"    -> Consumer processing order: '{order_id}' (Delivery attempt #{msg.receive_count})")

        # Step 1: Idempotency check
        if order_id in self.processed_order_ids:
            print(f"    [IDEMPOTENCY GUARD] Order '{order_id}' was ALREADY processed! Skipping duplicate charge.")
            return True  # Safe to delete duplicate

        # Step 2: Simulate crash before DB commit or SQS delete
        if should_crash:
            print(f"    [CRASH INJECTION] Worker suddenly died (OOM / panic / power failure) before committing!")
            raise RuntimeError(f"Simulated crash on order {order_id}")

        # Step 3: Execute business side effect
        self.processed_order_ids.add(order_id)
        self.processed_bank_charges.append({"order_id": order_id, "amount": 99.00})
        print(f"    [COMMITTED] Successfully charged customer $99.00 for order '{order_id}'.")
        return True


def run_experiment():
    print("=" * 65)
    print("      SQS Visibility Timeout & Idempotent Consumer Lab           ")
    print("=" * 65)

    dlq = MockSQSQueue(name="Orders-DeadLetterQueue.fifo", visibility_timeout_sec=5.0)
    queue = MockSQSQueue(
        name="Orders-PrimaryQueue",
        visibility_timeout_sec=1.5,
        max_receive_count=2,
        dlq=dlq
    )

    consumer = IdempotentPaymentConsumer()

    # Step 1: Send a message to SQS
    print("\n--- Phase 1: Producer sends message to SQS ---")
    msg_id = queue.send_message("ORDER-88219")
    print(f"Message published to '{queue.name}' with MessageId: {msg_id}")
    print(f"Queue depth (approx visible): {queue.approximate_number_of_messages()}")

    # Step 2: Worker receives message, but crashes
    print("\n--- Phase 2: Worker 1 receives message, but crashes before DeleteMessage ---")
    msg1 = queue.receive_message()
    assert msg1 is not None
    print(f"Worker 1 checked out message {msg1.message_id}. Visibility timeout set to {queue.visibility_timeout_sec}s.")
    print(f"Queue depth visible immediately after checkout: {queue.approximate_number_of_messages()} (hidden from others)")

    try:
        consumer.process_message(msg1, should_crash=True)
        queue.delete_message(msg1.message_id)
    except RuntimeError:
        print("Worker 1 exited abruptly. Note: queue.delete_message() was NEVER called!")

    # Step 3: Observe visibility timeout expiration
    print("\n--- Phase 3: Waiting for Visibility Timeout to expire ---")
    print("Sleeping 2.0 seconds while SQS tracks in-flight timeout...")
    time.sleep(2.0)
    print(f"Queue depth after timeout: {queue.approximate_number_of_messages()} (Message is visible again!)")

    # Step 4: Worker 2 receives the reappeared message
    print("\n--- Phase 4: Worker 2 receives the reappeared message (Retry #2) ---")
    msg2 = queue.receive_message()
    assert msg2 is not None
    print(f"Worker 2 checked out message {msg2.message_id} (Attempt #{msg2.receive_count})")
    
    # Process successfully this time
    success = consumer.process_message(msg2, should_crash=False)
    if success:
        queue.delete_message(msg2.message_id)
        print(f"Worker 2 called DeleteMessage({msg2.message_id}). Message permanently acknowledged.")

    print(f"Final Primary Queue depth: {queue.approximate_number_of_messages()}")

    # Step 5: Test Poison Pill and Dead-Letter Queue
    print("\n--- Phase 5: Poison Pill and Dead-Letter Queue (DLQ) Eviction ---")
    poison_id = queue.send_message("CORRUPTED-PAYLOAD-999")
    print(f"Sent poison message '{poison_id}' into queue.")

    for attempt in range(1, 4):
        print(f"\nDelivery attempt {attempt} for poison message:")
        p_msg = queue.receive_message()
        if p_msg is None:
            print("  Primary queue returned None. Checking DLQ...")
            break
        print(f"  Worker received {p_msg.message_id} (Attempt {p_msg.receive_count}). Simulating failure...")
        time.sleep(1.6)  # Let visibility timeout expire

    print(f"\nFinal State:")
    print(f"  Primary Queue messages remaining: {len(queue.messages)}")
    print(f"  Dead-Letter Queue messages:        {len(dlq.messages)}")
    assert len(dlq.messages) == 1, "Poison message should have been moved to DLQ!"
    print(f"  DLQ Message Payload:               {[m.body for m in dlq.messages.values()]}")

    print("\n" + "=" * 65)
    print("First-Principles Realization:")
    print("In distributed systems, delivery is at-least-once.")
    print("Reliability requires: Visibility Timeout + DLQs + Idempotent Consumers.")
    print("=" * 65)


if __name__ == "__main__":
    run_experiment()
