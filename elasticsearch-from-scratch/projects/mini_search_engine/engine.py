"""
projects/mini_search_engine/engine.py - Capstone 3: Standalone Search Engine from Scratch.
Pure Python 3 standard library implementation of:
- Text Analysis (Tokenizer, Normalizer, Stop words)
- Positional Inverted Index (with term frequencies & offsets)
- Columnar Doc Values Store
- Probabilistic BM25 Relevance Scoring (k1=1.2, b=0.75)
- Boolean Query Engine (must, filter, should, must_not)
- Phrase Search with Slop
"""

import math
import re
from collections import defaultdict, Counter

class TextAnalyzer:
    STOPWORDS = {"a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
                 "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "with"}

    @classmethod
    def analyze(cls, text, remove_stopwords=True):
        if not text:
            return []
        raw_tokens = re.findall(r'\b[a-zA-Z0-9_\-\.]+\b', text.lower())
        if remove_stopwords:
            return [t for t in raw_tokens if t not in cls.STOPWORDS]
        return raw_tokens

class MiniSearchEngine:
    def __init__(self, k1=1.2, b=0.75):
        self.k1 = k1
        self.b = b
        self.documents = {}           # doc_id -> raw document dict
        self.doc_lengths = {}         # doc_id -> token count
        # Inverted index: term -> doc_id -> list of positions
        self.inverted_index = defaultdict(lambda: defaultdict(list))
        # Columnar Doc Values: field_name -> doc_id -> value
        self.doc_values = defaultdict(dict)

    def index(self, doc_id, doc_dict, text_fields=("title", "description")):
        self.documents[doc_id] = doc_dict

        # Collect text across specified fields
        combined_text = " ".join(str(doc_dict.get(f, "")) for f in text_fields)
        tokens = TextAnalyzer.analyze(combined_text, remove_stopwords=False)
        self.doc_lengths[doc_id] = len(tokens)

        # Build positional inverted index
        for pos, token in enumerate(tokens):
            if token not in TextAnalyzer.STOPWORDS:
                self.inverted_index[token][doc_id].append(pos)

        # Build Columnar Doc Values for all non-text or keyword fields
        for field, val in doc_dict.items():
            if not isinstance(val, (dict, list)):
                self.doc_values[field][doc_id] = val

    def _compute_bm25_term_score(self, term, doc_id, avgdl, N):
        positions = self.inverted_index[term].get(doc_id)
        if not positions:
            return 0.0
        tf = len(positions)
        df = len(self.inverted_index[term])
        # Lucene BM25 IDF
        idf = math.log(1.0 + (N - df + 0.5) / (df + 0.5))
        doc_len = self.doc_lengths[doc_id]
        len_norm = 1.0 - self.b + self.b * (doc_len / avgdl) if avgdl > 0 else 1.0
        tf_norm = (tf * (self.k1 + 1)) / (tf + self.k1 * len_norm)
        return idf * tf_norm

    def match_phrase(self, phrase, slop=0):
        tokens = TextAnalyzer.analyze(phrase, remove_stopwords=False)
        if not tokens:
            return set()
        first = tokens[0]
        if first not in self.inverted_index:
            return set()
        candidate_docs = set(self.inverted_index[first].keys())
        for t in tokens[1:]:
            candidate_docs.intersection_update(self.inverted_index[t].keys())

        matched_docs = set()
        for doc_id in candidate_docs:
            pos_lists = [self.inverted_index[t][doc_id] for t in tokens]
            # Verify relative adjacent positions within slop window
            for p0 in pos_lists[0]:
                curr = p0
                valid = True
                for next_list in pos_lists[1:]:
                    allowed = [p for p in next_list if 0 < (p - curr) <= (1 + slop)]
                    if not allowed:
                        valid = False
                        break
                    curr = allowed[0]
                if valid:
                    matched_docs.add(doc_id)
                    break
        return matched_docs

    def search(self, query=None, must=None, filter_dict=None, should=None, must_not=None, size=10):
        N = len(self.documents)
        if N == 0:
            return []
        avgdl = sum(self.doc_lengths.values()) / float(N)

        must_terms = TextAnalyzer.analyze(must or query or "")
        should_terms = TextAnalyzer.analyze(should or "")
        must_not_terms = TextAnalyzer.analyze(must_not or "")

        # 1. Start with all documents if query is empty, else find matching must terms
        if must_terms:
            candidates = set(self.documents.keys())
            for t in must_terms:
                matching_docs = set(self.inverted_index[t].keys())
                candidates.intersection_update(matching_docs)
        else:
            candidates = set(self.documents.keys())

        # 2. Exclude must_not
        for t in must_not_terms:
            candidates.difference_update(self.inverted_index[t].keys())

        # 3. Apply binary filter context
        if filter_dict:
            for field, target_val in filter_dict.items():
                if isinstance(target_val, tuple) and len(target_val) == 2:
                    # Range filter (min, max)
                    low, high = target_val
                    candidates = {
                        d for d in candidates
                        if (low is None or self.doc_values[field].get(d, 0) >= low) and
                           (high is None or self.doc_values[field].get(d, 0) <= high)
                    }
                else:
                    candidates = {d for d in candidates if self.doc_values[field].get(d) == target_val}

        # 4. Score matching documents using BM25
        results = []
        for doc_id in candidates:
            score = 0.0
            for t in must_terms:
                score += self._compute_bm25_term_score(t, doc_id, avgdl, N)
            for t in should_terms:
                # Should acts as a score booster
                score += self._compute_bm25_term_score(t, doc_id, avgdl, N) * 1.5

            results.append((doc_id, round(score, 4), self.documents[doc_id]))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:size]
