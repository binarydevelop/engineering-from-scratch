#!/usr/bin/env python3
"""
Unit Tests for Delivery Service Domain Logic
Runs in isolation with zero network or database dependencies.
Fast feedback test stage (Phase 24).
"""

import unittest
from typing import Dict, Any


def validate_order_payload(payload: Dict[str, Any]) -> Tuple_Bool_Msg:
    email = payload.get("customer_email")
    amount = payload.get("amount_cents")

    if not email or "@" not in email:
        return False, "Invalid customer email address"
    if amount is None or not isinstance(amount, int) or amount <= 0:
        return False, "Amount must be a positive integer in cents"
    if amount > 10_000_00:  # $10,000 max single order limit
        return False, "Order amount exceeds single transaction safety threshold"
    return True, "Valid"


Tuple_Bool_Msg = tuple[bool, str]


class TestOrderDomainLogic(unittest.TestCase):
    def test_valid_order_payload(self):
        valid_payload = {"customer_email": "alice@example.com", "amount_cents": 2500}
        is_valid, msg = validate_order_payload(valid_payload)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "Valid")

    def test_missing_or_invalid_email(self):
        invalid_payloads = [
            {"customer_email": "", "amount_cents": 1000},
            {"customer_email": "invalid-email-format", "amount_cents": 1000},
            {"amount_cents": 1000}
        ]
        for p in invalid_payloads:
            is_valid, _ = validate_order_payload(p)
            self.assertFalse(is_valid, f"Expected failure for payload: {p}")

    def test_invalid_amount(self):
        invalid_amounts = [0, -500, "2500", None, 10_000_001]
        for amt in invalid_amounts:
            payload = {"customer_email": "bob@example.com", "amount_cents": amt}
            is_valid, _ = validate_order_payload(payload)
            self.assertFalse(is_valid, f"Expected failure for amount: {amt}")


if __name__ == "__main__":
    unittest.main()
