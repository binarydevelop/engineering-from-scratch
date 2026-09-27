"""
Tests for Tiny Query Planner.
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from planner import QueryPlanner, TableStats


class TestQueryPlanner(unittest.TestCase):

    def setUp(self):
        self.planner = QueryPlanner()

    def test_high_selectivity_chooses_index_scan(self):
        # 100,000 rows, 1,000 pages (8MB)
        # Selectivity = 0.001 (returns 100 rows)
        table = TableStats("orders", total_rows=100000, total_pages=1000, has_index=True)
        strategy, cost = self.planner.choose_scan(table, selectivity=0.001)
        self.assertEqual(strategy, "Index Scan")
        self.assertLess(cost, self.planner.cost_seq_scan(table))

    def test_low_selectivity_chooses_seq_scan(self):
        # Selectivity = 0.40 (returns 40,000 rows)
        # Index scan would cause 40,000 random page reads, which is much slower than reading 1,000 pages sequentially!
        table = TableStats("orders", total_rows=100000, total_pages=1000, has_index=True)
        strategy, cost = self.planner.choose_scan(table, selectivity=0.40)
        self.assertEqual(strategy, "Sequential Scan")
        self.assertLess(cost, self.planner.cost_index_scan(table, selectivity=0.40))

    def test_small_outer_chooses_nested_loop(self):
        # 10 outer rows joining into 100,000 inner rows with index
        outer = TableStats("departments", total_rows=10, total_pages=1)
        inner = TableStats("employees", total_rows=100000, total_pages=1000, has_index=True)
        join_type, cost = self.planner.choose_join(outer, inner, inner_has_join_index=True)
        self.assertEqual(join_type, "Nested Loop Join")

    def test_large_unsorted_chooses_hash_join(self):
        # 50,000 outer rows joining into 100,000 inner rows with NO index
        outer = TableStats("orders", total_rows=50000, total_pages=500)
        inner = TableStats("line_items", total_rows=100000, total_pages=1000, has_index=False)
        join_type, cost = self.planner.choose_join(outer, inner, inner_has_join_index=False)
        self.assertEqual(join_type, "Hash Join")


if __name__ == "__main__":
    unittest.main()
