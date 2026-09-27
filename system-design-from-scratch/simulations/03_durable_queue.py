import time
import uuid
from typing import Dict, Any, Optional, List

class DurableQueue:
    def __init__(self, max_delivery_attempts: int = 3):
        self.max_attempts = max_delivery_attempts
        self.messages: Dict[str, Dict[str, Any]] = {}
        self.dlq: List[Dict[str, Any]] = []

    def publish(self, payload: Any) -> str:
        msg_id = f"msg_{uuid.uuid4().hex[:8]}"
        self.messages[msg_id] = {
            "id": msg_id,
            "payload": payload,
            "attempts": 0,
            "visible_at": time.time(),
            "status": "AVAILABLE"
        }
        return msg_id

    def poll(self, visibility_timeout_sec: float = 5.0) -> Optional[Dict[str, Any]]:
        now = time.time()
        for msg_id, msg in self.messages.items():
            if msg["status"] == "AVAILABLE" and now >= msg["visible_at"]:
                msg["attempts"] += 1
                if msg["attempts"] > self.max_attempts:
                    msg["status"] = "DEAD_LETTER"
                    self.dlq.append(dict(msg))
                    continue
                msg["visible_at"] = now + visibility_timeout_sec
                return dict(msg)
        return None

    def ack(self, msg_id: str) -> bool:
        if msg_id in self.messages:
            del self.messages[msg_id]
            return True
        return False

    def nack(self, msg_id: str):
        if msg_id in self.messages:
            self.messages[msg_id]["visible_at"] = time.time()  # Immediately visible
