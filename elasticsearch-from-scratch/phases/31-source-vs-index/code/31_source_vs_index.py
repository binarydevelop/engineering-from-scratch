#!/usr/bin/env python3

class ThreeStorageChannels:
    def __init__(self):
        self.inverted_index = {} # term -> [doc_ids]
        self.doc_values = {}     # doc_id -> column values
        self.source_store = {}   # doc_id -> raw compressed string

    def index(self, doc_id, doc_dict):
        # 1. Store raw source
        self.source_store[doc_id] = str(doc_dict)
        # 2. Build inverted index for title
        for word in doc_dict.get("title", "").lower().split():
            self.inverted_index.setdefault(word, []).append(doc_id)
        # 3. Build doc values for price
        self.doc_values[doc_id] = doc_dict.get("price")

if __name__ == "__main__":
    store = ThreeStorageChannels()
    doc = {"id": 1, "title": "Elasticsearch Guide", "price": 45.0}
    store.index(1, doc)

    print("Channel 1: Inverted Index (for search):", store.inverted_index)
    print("Channel 2: Doc Values (for sort/agg):   ", store.doc_values)
    print("Channel 3: Stored _source (for display):", store.source_store)
