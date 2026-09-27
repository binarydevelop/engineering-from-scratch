#!/usr/bin/env python3
import math

class BM25:
    def __init__(self, corpus, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = {k: v.lower().split() for k, v in corpus.items()}
        self.N = len(corpus)
        self.doc_lens = {k: len(v) for k, v in self.corpus.items()}
        self.avgdl = sum(self.doc_lens.values()) / self.N if self.N > 0 else 1.0

        # Compute document frequencies
        self.df = {}
        for words in self.corpus.values():
            for w in set(words):
                self.df[w] = self.df.get(w, 0) + 1

    def idf(self, term):
        n = self.df.get(term, 0)
        # Lucene BM25 IDF formula
        return math.log(1.0 + (self.N - n + 0.5) / (n + 0.5))

    def score_term(self, term, doc_id):
        words = self.corpus[doc_id]
        tf = words.count(term)
        if tf == 0:
            return 0.0
        doc_len = self.doc_lens[doc_id]
        idf = self.idf(term)
        numerator = tf * (self.k1 + 1)
        denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
        return idf * (numerator / denominator)

if __name__ == "__main__":
    corpus = {
        "doc1": "elasticsearch is a distributed search engine",
        "doc2": "elasticsearch elasticsearch elasticsearch distributed",
        "doc3": "redis is an in-memory caching key value database"
    }
    bm = BM25(corpus)
    print(f"Corpus avgdl: {bm.avgdl:.2f} words")
    print(f"IDF('elasticsearch'): {bm.idf('elasticsearch'):.4f}\n")
    print("Scores for term 'elasticsearch':")
    for doc_id in corpus:
        score = bm.score_term("elasticsearch", doc_id)
        print(f"  {doc_id}: score = {score:.4f} (length = {bm.doc_lens[doc_id]})")
