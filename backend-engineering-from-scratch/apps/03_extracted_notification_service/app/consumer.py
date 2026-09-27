"""
Notification consumer pipeline supporting retries, idempotency, and DLQ routing.
"""

from typing import Dict, Any, List
from dedup import IdempotencyStore
from delivery import NotificationSender, DeliveryProviderError

class NotificationConsumer:
    def __init__(self, max_retries: int = 3):
        self.idempotency_store = IdempotencyStore()
        self.sender = NotificationSender()
        self.max_retries = max_retries
        self.dlq: List[Dict[str, Any]] = []
        self.retry_counts: Dict[str, int] = {}

    def process_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        event_id = event["id"]

        # 1. Idempotency Check
        if self.idempotency_store.is_processed(event_id):
            return {"status": "SKIPPED_DUPLICATE", "event_id": event_id}

        # 2. Outbound Delivery with Retries
        attempts = 0
        while attempts < self.max_retries:
            try:
                attempts += 1
                self.sender.send(event["recipient"], event["message"])
                self.idempotency_store.mark_processed(event_id)
                return {"status": "DELIVERED", "event_id": event_id, "attempts": attempts}
            except DeliveryProviderError as exc:
                self.retry_counts[event_id] = attempts
                if attempts >= self.max_retries:
                    # 3. Route to Dead-Letter Queue
                    dlq_record = {
                        "event": event,
                        "error": str(exc),
                        "attempts": attempts,
                        "status": "DLQ_POISON"
                    }
                    self.dlq.append(dlq_record)
                    return {"status": "FAILED_TO_DLQ", "event_id": event_id, "error": str(exc)}

        return {"status": "UNREACHABLE"}
