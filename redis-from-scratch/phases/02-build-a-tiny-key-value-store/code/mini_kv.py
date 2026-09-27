#!/usr/bin/env python3
class MiniKV:
    def __init__(self):
        self._store = {}

    def set(self, key: str, value: str) -> str:
        self._store[key] = value
        return "OK"

    def get(self, key: str):
        return self._store.get(key, None)

    def delete(self, key: str) -> int:
        if key in self._store:
            del self._store[key]
            return 1
        return 0

    def exists(self, key: str) -> int:
        return 1 if key in self._store else 0

if __name__ == "__main__":
    kv = MiniKV()
    print("Testing MiniKV operations:")
    print("SET user:1 'Tushar':", kv.set("user:1", "Tushar"))
    print("GET user:1:", kv.get("user:1"))
    print("EXISTS user:1:", kv.exists("user:1"))
    print("DELETE user:1:", kv.delete("user:1"))
    print("GET user:1 (after delete):", kv.get("user:1"))
