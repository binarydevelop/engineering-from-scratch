"""
Lesson 201: B+ Tree Storage Engine and Buffer Pool
Implements page-based node routing and LRU buffer pool management.
"""
from typing import Dict, Any, List, Optional
from collections import OrderedDict

class BufferPoolManager:
    def __init__(self, capacity_pages: int = 3):
        self.capacity = capacity_pages
        self.pages: OrderedDict[int, Dict[str, Any]] = OrderedDict()
        self.dirty_pages: set = set()

    def get_page(self, page_id: int) -> Optional[Dict[str, Any]]:
        if page_id in self.pages:
            self.pages.move_to_end(page_id)
            return self.pages[page_id]
        return None

    def put_page(self, page_id: int, data: Dict[str, Any], is_dirty: bool = False):
        if page_id in self.pages:
            self.pages.move_to_end(page_id)
        else:
            if len(self.pages) >= self.capacity:
                evicted_id, _ = self.pages.popitem(last=False)
                self.dirty_pages.discard(evicted_id)
        self.pages[page_id] = data
        if is_dirty:
            self.dirty_pages.add(page_id)

class PhaseComponent:
    def __init__(self):
        self.name = "B+ Tree Storage Engine and Buffer Pool"
        self.buffer_pool = BufferPoolManager(capacity_pages=3)
        self.metrics = {"operations_total": 0, "errors_total": 0}

    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        self.metrics["operations_total"] += 1
        if not isinstance(payload, dict):
            self.metrics["errors_total"] += 1
            raise ValueError("Payload must be a dictionary")
        if payload.get("trigger_error"):
            self.metrics["errors_total"] += 1
            raise RuntimeError("Buffer pool eviction failure")

        page_id = payload.get("page_id", 101)
        data = payload.get("page_data", {"keys": [10, 20, 30]})
        self.buffer_pool.put_page(page_id, data, is_dirty=True)

        return {
            "status": "success",
            "phase": 201,
            "cached_pages": list(self.buffer_pool.pages.keys()),
            "dirty_pages": list(self.buffer_pool.dirty_pages)
        }

    def get_telemetry(self) -> Dict[str, Any]:
        return {"component": self.name, "metrics": self.metrics}
