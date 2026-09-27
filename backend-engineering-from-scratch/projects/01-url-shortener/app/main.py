"""
Project: URL Shortener Service
"""
from typing import Optional, Dict, Any, List, Set, Tuple, Union, Callable
class URLShortener:
    BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def __init__(self):
        self.db = {}
        self.cache = {}
        self.counter = 100000

    def encode(self, num: int) -> str:
        if num == 0:
            return self.BASE62[0]
        arr = []
        base = len(self.BASE62)
        while num:
            rem = num % base
            num = num // base
            arr.append(self.BASE62[rem])
        arr.reverse()
        return "".join(arr)

    def shorten(self, url: str) -> str:
        self.counter += 1
        code = self.encode(self.counter)
        record = {"code": code, "url": url, "clicks": 0}
        self.db[code] = record
        self.cache[code] = url
        return code

    def resolve(self, code: str) -> Optional[str]:
        # Cache hit
        if code in self.cache:
            self.db[code]["clicks"] += 1
            return self.cache[code]
        # Database fallback
        if code in self.db:
            url = self.db[code]["url"]
            self.cache[code] = url
            self.db[code]["clicks"] += 1
            return url
        return None
