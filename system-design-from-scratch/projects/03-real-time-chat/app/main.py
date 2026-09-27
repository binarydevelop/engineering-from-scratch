import time
from typing import Dict, List, Set, Optional, Any

class RealTimeChatPlatform:
    def __init__(self):
        self.rooms: Dict[str, Set[str]] = {}
        self.history: Dict[str, List[Dict[str, Any]]] = {}
        self.presence: Dict[str, float] = {}

    def join_room(self, room_id: str, user_id: str):
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
            self.history[room_id] = []
        self.rooms[room_id].add(user_id)
        self.presence[user_id] = time.time()

    def send_message(self, room_id: str, sender_id: str, content: str) -> Dict[str, Any]:
        msg = {
            "id": f"msg_{len(self.history.get(room_id, [])) + 1}",
            "sender": sender_id,
            "content": content,
            "timestamp": time.time()
        }
        if room_id in self.rooms:
            self.history[room_id].append(msg)
            self.presence[sender_id] = time.time()
        return msg

    def is_user_online(self, user_id: str, timeout_sec: float = 60.0) -> bool:
        last = self.presence.get(user_id)
        return last is not None and (time.time() - last) <= timeout_sec
