"""
Project: Real-Time Chat Backend
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class ChatRoomManager:
    def __init__(self):
        self.rooms = {}
        self.history = {}

    def join(self, room_id: str, user_id: str):
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
            self.history[room_id] = []
        self.rooms[room_id].add(user_id)

    def broadcast(self, room_id: str, sender: str, text: str) -> int:
        if room_id not in self.rooms:
            return 0
        msg = {"sender": sender, "text": text}
        self.history[room_id].append(msg)
        return len(self.rooms[room_id])
