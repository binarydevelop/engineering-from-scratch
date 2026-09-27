#!/usr/bin/env python3
"""
simulations/idempotency_risk.py
Demonstrates the fundamental uncertainty of remote communication (Two Generals Problem)
and how response packet loss leads to catastrophic duplicate business transactions
without idempotency keys.

Scenario:
  Client initiates a $100 payment.
  Server executes transaction, deducts funds.
  Network drops the HTTP 200 OK response packet.
  Client timeout fires -> Client retries payment.
"""

from dataclasses import dataclass
from typing import Dict, Optional, Tuple


@dataclass
class PaymentResponse:
    status_code: int
    message: str
    transaction_id: str


class PaymentServer:
    def __init__(self):
        self.ledger: Dict[str, float] = {"user_alice": 1000.0}
        self.processed_idempotency_keys: Dict[str, PaymentResponse] = {}
        self.total_deductions_count = 0

    def process_payment(
        self,
        account: str,
        amount: float,
        idempotency_key: Optional[str] = None,
    ) -> PaymentResponse:
        """Processes payment. If idempotency_key is provided and already seen, returns cached result."""
        if idempotency_key and idempotency_key in self.processed_idempotency_keys:
            # Idempotent replay: Do NOT deduct funds again!
            return self.processed_idempotency_keys[idempotency_key]

        # Execute business logic
        self.ledger[account] -= amount
        self.total_deductions_count += 1
        tx_id = f"tx_{self.total_deductions_count:04d}"

        response = PaymentResponse(
            status_code=200,
            message=f"Successfully charged ${amount:.2f}",
            transaction_id=tx_id,
        )

        if idempotency_key:
            self.processed_idempotency_keys[idempotency_key] = response

        return response


def simulate_payment_attempt(
    server: PaymentServer,
    idempotency_key: Optional[str],
    drop_response_on_first_try: bool = True,
) -> Tuple[int, float]:
    """Simulates a client sending a payment, experiencing response packet drop, and retrying."""
    account = "user_alice"
    amount = 100.0

    # Attempt 1
    resp1 = server.process_payment(account, amount, idempotency_key)

    if drop_response_on_first_try:
        # Simulate network drop of return packet
        resp1 = None  # Client gets socket timeout!

    # Client retry (Attempt 2)
    resp2 = server.process_payment(account, amount, idempotency_key)

    return server.total_deductions_count, server.ledger[account]


if __name__ == "__main__":
    print("Network Uncertainty & Idempotency Risk Simulation:")
    print("=" * 65)

    # Experiment A: Flawed System WITHOUT Idempotency Keys
    srv_a = PaymentServer()
    deductions_a, balance_a = simulate_payment_attempt(srv_a, idempotency_key=None)
    print("Experiment A: Retrying payment WITHOUT idempotency key:")
    print(f"  Initial Balance: $1000.00 | Intended Charge: $100.00")
    print(f"  Total Server Deductions Executed: {deductions_a} times!")
    print(f"  Final Account Balance:            ${balance_a:.2f}")
    assert deductions_a == 2, "Duplicate deduction did not occur!"
    print("  --> RESULT: DISASTER! Client was charged twice for a single purchase.")

    print("\n" + "-" * 65 + "\n")

    # Experiment B: Resilient System WITH Idempotency Keys
    srv_b = PaymentServer()
    key = "order_req_unique_uuid_987654"
    deductions_b, balance_b = simulate_payment_attempt(srv_b, idempotency_key=key)
    print("Experiment B: Retrying payment WITH idempotency key:")
    print(f"  Initial Balance: $1000.00 | Intended Charge: $100.00")
    print(f"  Total Server Deductions Executed: {deductions_b} time!")
    print(f"  Final Account Balance:            ${balance_b:.2f}")
    assert deductions_b == 1, "Idempotency failed!"
    assert balance_b == 900.0, "Balance incorrect!"
    print("  --> RESULT: SUCCESS! Server recognized retry and prevented duplicate charge.")

    print("\nSUCCESS: Network retry idempotency risk demonstrated.")
