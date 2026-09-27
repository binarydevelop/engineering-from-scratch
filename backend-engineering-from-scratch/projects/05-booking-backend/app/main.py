"""
Project: Reservation Booking Engine
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
import time

class BookingEngine:
    def __init__(self, hold_ttl_seconds: float = 0.5):
        self.slots = {"slot_10": {"status": "AVAILABLE", "hold_until": 0, "booked_by": None}}
        self.hold_ttl_seconds = hold_ttl_seconds

    def hold_slot(self, slot_id: str, user_id: str) -> bool:
        now = time.time()
        slot = self.slots.get(slot_id)
        if not slot:
            raise KeyError("Slot not found")

        # Can hold if AVAILABLE or previous hold expired
        if slot["status"] == "AVAILABLE" or (slot["status"] == "HELD" and now > slot["hold_until"]):
            slot["status"] = "HELD"
            slot["hold_until"] = now + self.hold_ttl_seconds
            slot["booked_by"] = user_id
            return True
        return False

    def confirm_booking(self, slot_id: str, user_id: str) -> bool:
        now = time.time()
        slot = self.slots.get(slot_id)
        if not slot:
            raise KeyError("Slot not found")

        if slot["status"] == "HELD" and slot["booked_by"] == user_id and now <= slot["hold_until"]:
            slot["status"] = "BOOKED"
            return True
        return False
