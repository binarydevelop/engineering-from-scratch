"""
Project: E-Commerce Transaction Backend
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class ECommerceService:
    def __init__(self):
        self.inventory = {"prod_1": 1}
        self.orders = {}
        self.outbox = []

    def place_order(self, order_id: str, product_id: str, quantity: int) -> dict:
        # Atomic consistency boundary
        current_stock = self.inventory.get(product_id, 0)
        if current_stock < quantity:
            raise ValueError("Insufficient stock")

        # Deduct stock and commit order
        self.inventory[product_id] -= quantity
        order = {"id": order_id, "product_id": product_id, "quantity": quantity, "status": "CONFIRMED"}
        self.orders[order_id] = order

        # Insert Transactional Outbox event
        self.outbox.append({
            "event": "OrderPlaced",
            "order_id": order_id,
            "processed": False
        })
        return order
