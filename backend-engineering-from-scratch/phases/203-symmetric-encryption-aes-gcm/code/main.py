"""
Lesson 203: Symmetric Encryption and AEAD
Implements AEAD envelope model with nonce/IV, ciphertext, and authentication tags.
"""
from typing import Dict, Any
import hashlib
import os

class PhaseComponent:
    def __init__(self, key: bytes = b"0123456789abcdef0123456789abcdef"):
        self.name = "Symmetric Encryption and Authenticated Encryption (AEAD)"
        self.key = key
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def encrypt(self, plaintext: str, associated_data: str = "") -> Dict[str, str]:
        """Simulates AEAD envelope (Nonce + Ciphertext + Tag)."""
        nonce = os.urandom(12).hex()
        # Simulated authenticated encryption
        raw = f"{nonce}:{associated_data}:{plaintext}".encode("utf-8")
        tag = hashlib.sha256(self.key + raw).hexdigest()[:32]
        ciphertext = plaintext.encode("utf-8").hex()
        return {"nonce": nonce, "ciphertext": ciphertext, "tag": tag, "aad": associated_data}

    def decrypt(self, envelope: Dict[str, str]) -> str:
        nonce = envelope["nonce"]
        ciphertext = envelope["ciphertext"]
        expected_tag = envelope["tag"]
        aad = envelope.get("aad", "")
        plaintext = bytes.fromhex(ciphertext).decode("utf-8")

        raw = f"{nonce}:{aad}:{plaintext}".encode("utf-8")
        actual_tag = hashlib.sha256(self.key + raw).hexdigest()[:32]
        if actual_tag != expected_tag:
            raise ValueError("Authentication tag mismatch! Data has been tampered with.")
        return plaintext

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Key decryption failure")

        pt = payload.get("plaintext", "customer_credit_card_data")
        env = self.encrypt(pt, payload.get("aad", "tenant_id=42"))
        decrypted = self.decrypt(env)

        return {
            "status": "success",
            "phase": 203,
            "envelope": env,
            "decrypted_matches": (decrypted == pt)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
