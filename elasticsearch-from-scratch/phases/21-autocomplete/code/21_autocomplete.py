#!/usr/bin/env python3
from collections import defaultdict
import time

class EdgeNGramIndex:
    def __init__(self, min_gram=2, max_gram=5):
        self.min_gram = min_gram
        self.max_gram = max_gram
        self.index = defaultdict(list)

    def add(self, doc_id, text):
        for word in text.lower().split():
            length = len(word)
            for g in range(self.min_gram, min(self.max_gram + 1, length + 1)):
                gram = word[:g]
                self.index[gram].append((doc_id, text))

    def suggest(self, prefix):
        return self.index.get(prefix.lower(), [])

if __name__ == "__main__":
    catalog = EdgeNGramIndex()
    items = ["mechanical keyboard", "ergonomic mouse", "membrane switch", "monitor stand"]
    for i, it in enumerate(items):
        catalog.add(i, it)

    print("Index Terms generated for Edge N-Grams:")
    for k in sorted(catalog.index.keys()):
        print(f"  '{k}' -> {[it for _, it in catalog.index[k]]}")

    prefix = "mech"
    print(f"\nQuerying prefix '{prefix}':")
    print(catalog.suggest(prefix))
