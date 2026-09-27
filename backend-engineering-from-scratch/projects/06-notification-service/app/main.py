"""
Project: Notification Microservice
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class NotificationService:
    def __init__(self):
        self.primary_online = True
        self.delivered = []

    def send(self, recipient: str, message: str) -> dict:
        if self.primary_online:
            provider = "PrimaryProvider_SES"
        else:
            provider = "BackupProvider_SendGrid"

        record = {"recipient": recipient, "message": message, "provider": provider, "status": "DELIVERED"}
        self.delivered.append(record)
        return record
