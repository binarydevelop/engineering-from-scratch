"""
Workflow State Machine & Semantic Router (Phases 145-148).
Demonstrates when ordinary deterministic code is superior to an LLM agent:
1. Finite State Machine (FSM) with explicit state transitions.
2. Semantic Router categorizing intent into bounded handlers.
3. Planner / Executor decomposing goals into verifiable sequential steps.
"""

from typing import Dict, Any, Callable, List
from enum import Enum

class OrderState(Enum):
    COLLECT_ITEMS = "COLLECT_ITEMS"
    VALIDATE_INVENTORY = "VALIDATE_INVENTORY"
    PROCESS_PAYMENT = "PROCESS_PAYMENT"
    DISPATCH_ORDER = "DISPATCH_ORDER"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class OrderStateMachine:
    """Deterministic state machine governing e-commerce checkout flow."""
    def __init__(self):
        self.state = OrderState.COLLECT_ITEMS
        self.order_data: Dict[str, Any] = {}

    def transition(self, action: str, payload: Dict[str, Any]) -> OrderState:
        if self.state == OrderState.COLLECT_ITEMS:
            if action == "add_items":
                self.order_data["items"] = payload.get("items", [])
                self.state = OrderState.VALIDATE_INVENTORY

        elif self.state == OrderState.VALIDATE_INVENTORY:
            if action == "inventory_ok":
                self.state = OrderState.PROCESS_PAYMENT
            else:
                self.state = OrderState.FAILED

        elif self.state == OrderState.PROCESS_PAYMENT:
            if action == "payment_success":
                self.state = OrderState.DISPATCH_ORDER
            else:
                self.state = OrderState.FAILED

        elif self.state == OrderState.DISPATCH_ORDER:
            if action == "dispatched":
                self.state = OrderState.COMPLETED

        return self.state

class SemanticRouter:
    """Fast keyword/embedding routing mapping user queries to bounded handlers."""
    def __init__(self):
        self.routes: Dict[str, List[str]] = {
            "billing": ["invoice", "charge", "refund", "credit card", "price"],
            "technical_support": ["bug", "error", "crash", "timeout", "broken"],
            "general_faq": ["hello", "hours", "contact", "about", "location"]
        }

    def route(self, query: str) -> str:
        q_lower = query.lower()
        for category, keywords in self.routes.items():
            if any(k in q_lower for k in keywords):
                return category
        return "general_faq"
