"""
Project 06: Chaos & Incident Timeline Simulator.
"""
import time
from typing import List, Dict, Any

class IncidentSimulator:
    def __init__(self):
        self.events: List[Dict[str, Any]] = []

    def inject_failure(self, failure_type: str, component: str, duration_sec: int) -> Dict[str, Any]:
        event = {
            "timestamp": time.time(),
            "failure_type": failure_type,
            "component": component,
            "duration_sec": duration_sec,
            "status": "ACTIVE"
        }
        self.events.append(event)
        return event

    def generate_timeline(self) -> List[Dict[str, Any]]:
        return sorted(self.events, key=lambda x: x["timestamp"])
