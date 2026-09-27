#!/usr/bin/env python3
from collections import defaultdict

class FieldedMiniIndex:
    def __init__(self):
        self.text_indexes = defaultdict(lambda: defaultdict(list))
        self.exact_indexes = defaultdict(lambda: defaultdict(list))
        self.numeric_store = defaultdict(dict)
        self.docs = {}

    def index_document(self, doc_id, doc):
        self.docs[doc_id] = doc
        for field, value in doc.items():
            if isinstance(value, str):
                # Text tokenized index
                tokens = [t.lower() for t in value.split()]
                for t in set(tokens):
                    self.text_indexes[field][t].append(doc_id)
                # Exact keyword index
                self.exact_indexes[field][value].append(doc_id)
            elif isinstance(value, (int, float)):
                self.numeric_store[field][doc_id] = value

    def search_text(self, field, term):
        return self.text_indexes[field].get(term.lower(), [])

    def filter_range(self, field, min_val, max_val):
        hits = []
        for doc_id, val in self.numeric_store[field].items():
            if min_val <= val <= max_val:
                hits.append(doc_id)
        return hits

if __name__ == "__main__":
    idx = FieldedMiniIndex()
    idx.index_document(1, {"title": "Ergonomic Wireless Keyboard", "category": "electronics", "price": 99.0})
    idx.index_document(2, {"title": "Mechanical Gaming Keyboard", "category": "electronics", "price": 149.0})
    idx.index_document(3, {"title": "Ergonomic Office Chair", "category": "furniture", "price": 299.0})

    print("Search 'title:ergonomic' ->", idx.search_text("title", "ergonomic"))
    print("Filter 'price: 80 to 120' ->", idx.filter_range("price", 80.0, 120.0))
