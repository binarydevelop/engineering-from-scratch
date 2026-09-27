import time
from typing import Dict, Any, Optional

class URLShortenerService:
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self):
        self.db: Dict[str, Dict[str, Any]] = {}
        self.cache: Dict[str, str] = {}
        self.click_queue: list = []
        self.counter = 100000

    def encode(self, num: int) -> str:
        if num == 0:
            return self.BASE62[0]
        digits = []
        base = len(self.BASE62)
        while num > 0:
            digits.append(self.BASE62[num % base])
            num //= base
        return "".join(reversed(digits))

    def shorten(self, url: str) -> str:
        self.counter += 1
        code = self.encode(self.counter)
        record = {"code": code, "url": url, "clicks": 0, "created_at": time.time()}
        self.db[code] = record
        self.cache[code] = url
        return code

    def resolve(self, code: str) -> Optional[str]:
        # 1. Cache hit
        if code in self.cache:
            self.click_queue.append(code)
            return self.cache[code]
        # 2. Database query on cache miss
        if code in self.db:
            url = self.db[code]["url"]
            self.cache[code] = url
            self.click_queue.append(code)
            return url
        return None

    def process_clicks_worker(self) -> int:
        processed = 0
        while self.click_queue:
            code = self.click_queue.pop(0)
            if code in self.db:
                self.db[code]["clicks"] += 1
                processed += 1
        return processed
