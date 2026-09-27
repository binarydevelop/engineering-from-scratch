#!/usr/bin/env python3
import math
import re
from collections import defaultdict, Counter

class MiniSearchEngine:
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.docs = {}
        self.inverted_index = defaultdict(lambda: defaultdict(int)) # term -> doc_id -> tf
        self.doc_lens = {}
        self.doc_values = defaultdict(dict) # field -> doc_id -> value

    def _tokenize(self, text):
        return [t.lower() for t in re.findall(r'\b\w+\b', text)]

    def index_document(self, doc_id, doc):
        self.docs[doc_id] = doc
        tokens = self._tokenize(doc.get("text", ""))
        self.doc_lens[doc_id] = len(tokens)
        counts = Counter(tokens)
        for t, freq in counts.items():
            self.inverted_index[t][doc_id] = freq

        # Index doc values
        for f in ["category", "price", "status"]:
            if f in doc:
                self.doc_values[f][doc_id] = doc[f]

    def search(self, query_str, filter_cat=None, top_k=5):
        q_tokens = self._tokenize(query_str)
        N = len(self.docs)
        if N == 0 or not q_tokens:
            return []
        avgdl = sum(self.doc_lens.values()) / N

        # Find candidates
        candidates = set()
        for t in q_tokens:
            candidates.update(self.inverted_index[t].keys())

        # Apply filter context
        if filter_cat:
            candidates = {d for d in candidates if self.doc_values["category"].get(d) == filter_cat}

        scores = []
        for doc_id in candidates:
            doc_score = 0.0
            doc_len = self.doc_lens[doc_id]
            for t in q_tokens:
                tf = self.inverted_index[t].get(doc_id, 0)
                if tf > 0:
                    df = len(self.inverted_index[t])
                    idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
                    num = tf * (self.k1 + 1)
                    denom = tf + self.k1 * (1 - self.b + self.b * (doc_len / avgdl))
                    doc_score += idf * (num / denom)
            scores.append((doc_id, round(doc_score, 4), self.docs[doc_id]))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

if __name__ == "__main__":
    engine = MiniSearchEngine()
    engine.index_document(1, {"text": "Distributed search with inverted index", "category": "tech", "price": 45})
    engine.index_document(2, {"text": "Elasticsearch distributed cluster architecture", "category": "tech", "price": 85})
    engine.index_document(3, {"text": "Ergonomic leather chair for office", "category": "furniture", "price": 199})

    results = engine.search("distributed architecture", filter_cat="tech")
    print("Mini Search Engine Query Results (query='distributed architecture', filter='tech'):")
    for doc_id, score, doc in results:
        print(f"  [Doc {doc_id}] Score: {score:.4f} | {doc}")
