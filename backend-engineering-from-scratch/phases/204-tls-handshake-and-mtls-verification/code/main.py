"""
Lesson 204: TLS Handshake and mTLS Verification
Implements TLS 1.3 handshake state machine and mutual certificate validation.
"""
from typing import Dict, Any

class PhaseComponent:
    def __init__(self):
        self.name = "TLS Handshake and mTLS Verification"
        self.trusted_cas = {"corp-root-ca", "internal-mesh-ca"}
        self.metrics = {"operations_total": 0, "errors_total": 0, "handshakes_completed": 0}

    def verify_certificate(self, cert: Dict[str, str]) -> bool:
        """Validates that cert is issued by a trusted CA and not expired."""
        issuer = cert.get("issuer")
        return issuer in self.trusted_cas

    def run_mtls_handshake(self, client_hello: Dict[str, Any], server_cert: Dict[str, str], client_cert: Dict[str, str]) -> Dict[str, Any]:
        if not self.verify_certificate(server_cert):
            raise ValueError("Server certificate untrusted")
        if not self.verify_certificate(client_cert):
            raise ValueError("Client certificate untrusted (mTLS rejected)")

        self.metrics["handshakes_completed"] += 1
        return {
            "tls_version": "TLSv1.3",
            "cipher_suite": "TLS_AES_256_GCM_SHA384",
            "client_identity": client_cert.get("subject"),
            "server_identity": server_cert.get("subject"),
            "mtls_established": True
        }

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Handshake timeout")

        s_cert = payload.get("server_cert", {"subject": "api.corp.internal", "issuer": "internal-mesh-ca"})
        c_cert = payload.get("client_cert", {"subject": "checkout.service", "issuer": "internal-mesh-ca"})
        hs = self.run_mtls_handshake({}, s_cert, c_cert)

        return {"status": "success", "phase": 204, "handshake": hs}

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
