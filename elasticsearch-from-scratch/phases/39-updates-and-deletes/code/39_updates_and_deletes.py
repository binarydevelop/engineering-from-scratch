#!/usr/bin/env python3

class UpdateDeleteEngine:
    def __init__(self):
        self.doc_store = {} # id -> (version, data)
        self.total_inserts = 0
        self.total_deletions = 0

    def index(self, doc_id, data):
        if doc_id in self.doc_store:
            # Update: delete old + insert new
            old_ver, _ = self.doc_store[doc_id]
            self.total_deletions += 1
            new_ver = old_ver + 1
        else:
            new_ver = 1
        self.doc_store[doc_id] = (new_ver, data)
        self.total_inserts += 1
        return new_ver

    def stats(self):
        return {
            "active_docs": len(self.doc_store),
            "deleted_markers": self.total_deletions,
            "total_physical_writes": self.total_inserts
        }

if __name__ == "__main__":
    engine = UpdateDeleteEngine()
    print("Indexing Doc 1...")
    engine.index(1, {"price": 10})
    print("Updating Doc 1 (five times)...")
    for p in [20, 30, 40, 50, 60]:
        engine.index(1, {"price": p})
    print("Engine Stats:", engine.stats())
    print("Active docs: 1, but 5 deleted markers exist in storage!")
