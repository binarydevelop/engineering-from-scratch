#!/usr/bin/env python3
"""
Unit tests for MiniSearchEngine (Capstone 3).
"""

import unittest
from engine import MiniSearchEngine

class TestMiniSearchEngine(unittest.TestCase):
    def setUp(self):
        self.engine = MiniSearchEngine()
        self.docs = {
            1: {"title": "Distributed Search Architecture", "category": "tech", "price": 100},
            2: {"title": "Inverted Index and BM25 Relevance", "category": "tech", "price": 50},
            3: {"title": "Ergonomic Office Chair", "category": "furniture", "price": 250},
            4: {"title": "Distributed Systems in Practice", "category": "tech", "price": 80}
        }
        for d_id, doc in self.docs.items():
            self.engine.index(d_id, doc)

    def test_term_search(self):
        hits = self.engine.search("distributed")
        matched_ids = [h[0] for h in hits]
        self.assertIn(1, matched_ids)
        self.assertIn(4, matched_ids)
        self.assertNotIn(3, matched_ids)

    def test_filter_context(self):
        hits = self.engine.search("distributed", filter_dict={"category": "tech", "price": (70, 150)})
        matched_ids = [h[0] for h in hits]
        self.assertEqual(matched_ids, [1, 4])

    def test_phrase_search(self):
        matches = self.engine.match_phrase("distributed systems", slop=0)
        self.assertEqual(matches, {4})

    def test_must_not(self):
        hits = self.engine.search(must="distributed", must_not="systems")
        matched_ids = [h[0] for h in hits]
        self.assertIn(1, matched_ids)
        self.assertNotIn(4, matched_ids)

if __name__ == "__main__":
    unittest.main()
