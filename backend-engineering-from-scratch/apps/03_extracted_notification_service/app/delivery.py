"""
Outbound delivery adapter for email and SMS notifications.
"""

from typing import Dict, Any, List

class DeliveryProviderError(Exception):
    pass

class NotificationSender:
    def __init__(self):
        self.sent_log: List[Dict[str, Any]] = []
        self.should_fail = False

    def send(self, recipient: str, message: str) -> Dict[str, Any]:
        if self.should_fail:
            raise DeliveryProviderError("Downstream provider gateway timeout (504)")

        record = {
            "recipient": recipient,
            "message": message,
            "provider": "SES_Mock",
            "status": "SENT"
        }
        self.sent_log.append(record)
        return record
