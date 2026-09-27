"""
Lesson 205: Zero-Trust PASETO and Service Identity
Implements PASETO v4.public-style tokens and SPIFFE workload identity validation.
"""
from typing import Dict, Any
import json
import base64
import hashlib
import time

class PhaseComponent:
    def __init__(self, signing_secret: str = "spiffe_signing_master_key"):
        self.name = "Zero-Trust PASETO and Service Identity"
        self.signing_secret = signing_secret
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def issue_token(self, spiffe_id: str, claims: Dict[str, Any], ttl_sec: int = 3600) -> str:
        """Issues token with SPIFFE workload identity."""
        payload = {
            "sub": spiffe_id,
            "iat": time.time(),
            "exp": time.time() + ttl_sec,
            "claims": claims
        }
        raw_json = json.dumps(payload, sort_keys=True)
        sig = hashlib.sha256((self.signing_secret + raw_json).encode("utf-8")).hexdigest()
        b64_payload = base64.urlsafe_b64encode(raw_json.encode("utf-8")).decode("utf-8")
        return f"v4.public.{b64_payload}.{sig}"

    def verify_token(self, token: str) -> Dict[str, Any]:
        parts = token.split(".")
        if len(parts) != 4 or parts[0] != "v4" or parts[1] != "public":
            raise ValueError("Invalid PASETO header format")

        b64_payload, provided_sig = parts[2], parts[3]
        raw_json = base64.urlsafe_b64decode(b64_payload.encode("utf-8")).decode("utf-8")
        expected_sig = hashlib.sha256((self.signing_secret + raw_json).encode("utf-8")).hexdigest()

        if expected_sig != provided_sig:
            raise ValueError("Invalid token signature")

        data = json.loads(raw_json)
        if time.time() > data["exp"]:
            raise ValueError("Token expired")
        return data

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Token verification revoked")

        spiffe = payload.get("spiffe_id", "spiffe://prod.corp/sa/payment-service")
        token = self.issue_token(spiffe, {"role": "payment_processor"})
        verified = self.verify_token(token)

        return {
            "status": "success",
            "phase": 205,
            "token": token[:35] + "...",
            "spiffe_id": verified["sub"],
            "is_valid": True
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
