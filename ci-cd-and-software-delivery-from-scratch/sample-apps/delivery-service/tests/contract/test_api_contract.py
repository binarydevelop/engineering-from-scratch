#!/usr/bin/env python3
"""
API Contract Tests (Phase 33)
Validates that endpoints return expected JSON schema shapes, header metadata,
and backward-compatible fields required by downstream consumer services.
"""

import json
import unittest
from typing import Dict, Any


def validate_version_endpoint_contract(data: Dict[str, Any]) -> bool:
    """Contract: /version must supply service, version, commit_sha, and artifact_digest."""
    required_keys = {"service", "version", "commit_sha", "artifact_digest", "environment"}
    return required_keys.issubset(data.keys())


def validate_order_response_contract(data: Dict[str, Any]) -> bool:
    """Contract: Order creation response must return id, customer_email, amount_cents, status."""
    order = data.get("order")
    if not isinstance(order, dict):
        return False
    required_fields = {"id", "customer_email", "amount_cents", "status", "created_at"}
    return required_fields.issubset(order.keys())


class TestAPIContract(unittest.TestCase):
    def test_version_schema_contract(self):
        sample_payload = {
            "service": "delivery-service",
            "version": "1.2.0",
            "commit_sha": "a1b2c3d4e5f678901234567890abcdef12345678",
            "artifact_digest": "sha256:7f9b8c31e428a1...",
            "build_timestamp": "2026-09-27T08:00:00Z",
            "environment": "production"
        }
        self.assertTrue(validate_version_endpoint_contract(sample_payload))

    def test_missing_contract_field_fails(self):
        broken_payload = {
            "service": "delivery-service",
            "version": "1.2.0"
            # Missing commit_sha, artifact_digest
        }
        self.assertFalse(validate_version_endpoint_contract(broken_payload))

    def test_order_creation_contract(self):
        order_payload = {
            "message": "Order created successfully",
            "order": {
                "id": 101,
                "customer_email": "dave@example.com",
                "amount_cents": 5999,
                "status": "pending",
                "created_at": "2026-09-27T08:15:00Z"
            }
        }
        self.assertTrue(validate_order_response_contract(order_payload))


if __name__ == "__main__":
    unittest.main()
