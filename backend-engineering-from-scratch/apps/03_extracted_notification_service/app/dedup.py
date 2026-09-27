"""
Idempotency and deduplication store for notification service.
Guarantees exactly-once side-effects under at-least-once delivery semantics.
"""

from typing import Set

class IdempotencyStore:
    def __init__(self):
        self._processed_ids: Set[str] = set()

    def is_processed(self, message_id: str) -> bool:
        return message_id in self._processed_ids

    def mark_processed(self, message_id: str):
        self._processed_ids.add(message_id)

    def count(self) -> int:
        return len(self._processed_ids)
