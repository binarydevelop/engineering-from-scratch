#!/usr/bin/env python3
import math
from collections import Counter

class SimpleTFIDF:
    def __init__(self, corpus):
        self.corpus = {k: v.lower().split() for k, v in corpus.items()}
        self.N = len(corpus)
        self.df = Counter()
        for words in self.corpus.values():
            for term in set(words):
                self.df[term] += 1

    def idf(self, term):
        df_val = self.df.get(term, 0)
        if df_val == 0:
            return 0.0
        return math.log(1.0 + (self.N / df_val))

    def score(self, query, doc_id):
        words = self.corpus[doc_id]
        score = 0.0
        for q in query.lower().split():
            tf = words.count(q)
            score += tf * self.idf(q)
        return score

if __name__ == "__main__":
    docs = {
        1: "the quick brown fox jumps over the lazy dog",
        2: "the distributed architecture of elasticsearch clusters",
        3: "the cat sat on the mat"
    }
    tfidf = SimpleTFIDF(docs)
    print(f"Corpus size: {tfidf.N} docs")
    print(f"IDF('the'):           {tfidf.idf('the'):.4f} (Appears in 3/3 docs)")
    print(f"IDF('elasticsearch'): {tfidf.idf('elasticsearch'):.4f} (Appears in 1/3 docs)")

    q = "the elasticsearch"
    print(f"\nQuery: '{q}'")
    for doc_id in docs:
        s = tfidf.score(q, doc_id)
        print(f"  Doc {doc_id} score: {s:.4f}")
