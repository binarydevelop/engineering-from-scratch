import hashlib
from typing import List

class BloomFilter:
    def __init__(self, size: int = 1000, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str) -> List[int]:
        res = []
        for i in range(self.num_hashes):
            h = int(hashlib.md5(f"{item}:{i}".encode()).hexdigest(), 16)
            res.append(h % self.size)
        return res

    def add(self, item: str):
        for idx in self._hashes(item):
            self.bit_array[idx] = 1

    def contains(self, item: str) -> bool:
        return all(self.bit_array[idx] == 1 for idx in self._hashes(item))
