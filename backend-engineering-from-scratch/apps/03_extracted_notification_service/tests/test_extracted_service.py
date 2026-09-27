"""
Tests for Capstone 03: Extracted Notification Service.
"""

import os
import sys
import pytest

APP_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app")
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from consumer import NotificationConsumer

def test_successful_notification_delivery():
    consumer = NotificationConsumer()
    event = {
        "id": "evt_001",
        "recipient": "customer@example.com",
        "message": "Your order #1024 has shipped!"
    }

    result = consumer.process_event(event)
    assert result["status"] == "DELIVERED"
    assert len(consumer.sender.sent_log) == 1
    assert consumer.idempotency_store.is_processed("evt_001")

def test_idempotent_deduplication():
    consumer = NotificationConsumer()
    event = {
        "id": "evt_002",
        "recipient": "customer@example.com",
        "message": "Welcome bonus applied"
    }

    # First delivery
    res1 = consumer.process_event(event)
    assert res1["status"] == "DELIVERED"
    assert len(consumer.sender.sent_log) == 1

    # Second delivery (e.g. at-least-once redelivery from queue)
    res2 = consumer.process_event(event)
    assert res2["status"] == "SKIPPED_DUPLICATE"
    # Should NOT have sent another email!
    assert len(consumer.sender.sent_log) == 1

def test_dead_letter_queue_on_persistent_failure():
    consumer = NotificationConsumer(max_retries=3)
    consumer.sender.should_fail = True

    poison_event = {
        "id": "evt_poison_999",
        "recipient": "corrupt@example.com",
        "message": "Faulty payload"
    }

    result = consumer.process_event(poison_event)
    assert result["status"] == "FAILED_TO_DLQ"
    assert len(consumer.dlq) == 1
    assert consumer.dlq[0]["event"]["id"] == "evt_poison_999"
    assert consumer.dlq[0]["attempts"] == 3
