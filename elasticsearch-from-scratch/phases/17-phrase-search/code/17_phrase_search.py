#!/usr/bin/env python3
from collections import defaultdict

class PositionalIndex:
    def __init__(self):
        # term -> doc_id -> list of positions
        self.index = defaultdict(lambda: defaultdict(list))
        self.docs = {}

    def add_doc(self, doc_id, text):
        self.docs[doc_id] = text
        words = text.lower().split()
        for pos, word in enumerate(words):
            self.index[word][doc_id].append(pos)

    def match_phrase(self, phrase, slop=0):
        words = phrase.lower().split()
        if not words:
            return []
        first_term = words[0]
        candidate_docs = set(self.index[first_term].keys())
        for w in words[1:]:
            candidate_docs.intersection_update(self.index[w].keys())

        matches = []
        for doc_id in candidate_docs:
            if self._check_positions(doc_id, words, slop):
                matches.append(doc_id)
        return matches

    def _check_positions(self, doc_id, words, slop):
        pos_lists = [self.index[w][doc_id] for w in words]
        for p0 in pos_lists[0]:
            current = p0
            matched = True
            for next_list in pos_lists[1:]:
                valid = [p for p in next_list if 0 < (p - current) <= (1 + slop)]
                if not valid:
                    matched = False
                    break
                current = valid[0]
            if matched:
                return True
        return False

if __name__ == "__main__":
    idx = PositionalIndex()
    idx.add_doc(1, "distributed systems architecture in cloud")
    idx.add_doc(2, "distributed database storage systems design")
    idx.add_doc(3, "operating systems distributed across machines")

    print("Phrase: 'distributed systems' (slop=0) -> Docs:", idx.match_phrase("distributed systems", slop=0))
    print("Phrase: 'distributed systems' (slop=2) -> Docs:", idx.match_phrase("distributed systems", slop=2))
