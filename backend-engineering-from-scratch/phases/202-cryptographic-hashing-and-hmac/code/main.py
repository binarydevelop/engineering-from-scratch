"""
Lesson 202: Cryptographic Hashing and HMAC
Implements HMAC-SHA256 message signing and constant-time signature verification.
"""
from typing import Dict, Any
import hmac
import hashlib

class PhaseComponent:
    def __init__(self, secret_key: bytes = b"master_distributed_secret"):
        self.name = "Cryptographic Hashing and HMAC"
        self.secret_key = secret_key
        self.metrics = {"operations_total": 0, "errors_total": 0, "tamper_detected": 0}

    def sign_message(self, message: str) -> str:
        """Calculates HMAC-SHA256 hex digest."""
        return hmac.new(self.secret_key, message.encode("utf-8"), hashlib.sha256).hexdigest()

    def verify_signature(self, message: str, provided_signature: str) -> bool:
        """Verifies HMAC in constant time to prevent timing attacks."""
        expected = self.sign_message(message)
        # hmac.compare_digest avoids early-exit timing leaks
        is_valid = hmac.compare_digest(expected, provided_signature)
        if not is_valid:
            self.metrics["tamper_detected"] += 1
        return is_valid

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Cryptographic subsystem error")

        msg = payload.get("message", "order_id=500&amount=100")
        sig = self.sign_message(msg)
        is_valid = self.verify_signature(msg, sig)

        return {
            "status": "success",
            "phase": 202,
            "signature": sig,
            "verified": is_valid
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
