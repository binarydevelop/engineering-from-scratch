"""
Project: Webhook Delivery Platform
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
import hmac
import hashlib

class WebhookPlatform:
    def __init__(self, secret: str = "webhook_secret_key"):
        self.secret = secret
        self.deliveries = []
        self.dlq = []

    def sign_payload(self, body: str) -> str:
        return hmac.new(self.secret.encode(), body.encode(), hashlib.sha256).hexdigest()

    def deliver(self, url: str, body: str, max_retries: int = 2) -> dict:
        sig = self.sign_payload(body)
        delivery = {"url": url, "signature": sig, "status": "DELIVERED"}
        self.deliveries.append(delivery)
        return delivery
