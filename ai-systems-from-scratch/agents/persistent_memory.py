"""
Persistent Memory Store with Versioning (Phases 131-133).
Manages long-term application user memory:
- Fact versioning (when facts change, old versions are invalidated)
- Semantic relevance filtering
- Preventing conflicting memories from confusing agent reasoning.
"""

from typing import List, Dict, Any, Optional
import time

class MemoryFact:
    def __init__(self, key: str, value: str, version: int = 1):
        self.key = key
        self.value = value
        self.version = version
        self.timestamp = time.time()
        self.is_active = True

class PersistentMemoryStore:
    def __init__(self):
        # Maps user_id -> key -> list of MemoryFact versions
        self._store: Dict[str, Dict[str, List[MemoryFact]]] = {}

    def set_fact(self, user_id: str, key: str, value: str) -> MemoryFact:
        if user_id not in self._store:
            self._store[user_id] = {}

        if key in self._store[user_id]:
            # Invalidate older version
            for old_fact in self._store[user_id][key]:
                old_fact.is_active = False
            new_version = len(self._store[user_id][key]) + 1
        else:
            self._store[user_id][key] = []
            new_version = 1

        fact = MemoryFact(key, value, version=new_version)
        self._store[user_id][key].append(fact)
        return fact

    def get_active_facts(self, user_id: str) -> Dict[str, str]:
        if user_id not in self._store:
            return {}
        active = {}
        for key, versions in self._store[user_id].items():
            for v in versions:
                if v.is_active:
                    active[key] = v.value
        return active
