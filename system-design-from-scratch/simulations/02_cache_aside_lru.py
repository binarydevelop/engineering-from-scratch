import time
from collections import OrderedDict
from typing import Any, Callable, Optional, Dict

class LRUCacheAside:
    def __init__(self, capacity: int = 100, default_ttl_sec: float = 60.0):
        self.capacity = capacity
        self.default_ttl = default_ttl_sec
        self.cache: OrderedDict[str, Dict[str, Any]] = OrderedDict()
        self.hits = 0
        self.misses = 0

    def get(self, key: str, fetch_from_db_fn: Optional[Callable[[str], Any]] = None) -> Any:
        now = time.time()
        if key in self.cache:
            entry = self.cache[key]
            if now < entry["expires_at"]:
                self.hits += 1
                self.cache.move_to_end(key)
                return entry["value"]
            else:
                del self.cache[key]  # Expired

        self.misses += 1
        if fetch_from_db_fn:
            val = fetch_from_db_fn(key)
            if val is not None:
                self.set(key, val)
            return val
        return None

    def set(self, key: str, value: Any, ttl_sec: Optional[float] = None):
        if key in self.cache:
            self.cache.move_to_end(key)
        elif len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Evict oldest (LRU)

        ttl = ttl_sec if ttl_sec is not None else self.default_ttl
        self.cache[key] = {"value": value, "expires_at": time.time() + ttl}
