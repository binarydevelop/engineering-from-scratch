"""
Tiny Relational Query Planner & Cost Estimator.
Demonstrates:
  - Cost modeling based on disk I/O pages and CPU instruction cycles
  - Scan Selection: Sequential Scan vs Index Scan (Selectivity Thresholds)
  - Join Selection: Nested Loop vs Hash Join vs Merge Join
  - Reinforces: SQL = WHAT, Query Planner = HOW.
"""

from typing import Dict, Any, Tuple


class TableStats:
    def __init__(self, name: str, total_rows: int, total_pages: int, has_index: bool = False):
        self.name = name
        self.total_rows = total_rows
        self.total_pages = total_pages
        self.has_index = has_index


class QueryPlanner:
    def __init__(
        self,
        seq_page_cost: float = 1.0,
        random_page_cost: float = 4.0,
        cpu_tuple_cost: float = 0.01,
        cpu_operator_cost: float = 0.0025
    ):
        self.seq_page_cost = seq_page_cost
        self.random_page_cost = random_page_cost
        self.cpu_tuple_cost = cpu_tuple_cost
        self.cpu_operator_cost = cpu_operator_cost

    def cost_seq_scan(self, table: TableStats) -> float:
        """
        Sequential Scan Cost:
        Cost = (pages * seq_page_cost) + (rows * cpu_tuple_cost)
        """
        disk_cost = table.total_pages * self.seq_page_cost
        cpu_cost = table.total_rows * self.cpu_tuple_cost
        return round(disk_cost + cpu_cost, 2)

    def cost_index_scan(self, table: TableStats, selectivity: float) -> float:
        """
        Index Scan Cost:
        Estimates B-Tree traversal + random heap page fetches for matching tuples.
        Cost = (btree_depth * random_cost) + (matching_rows * (random_page_cost + cpu_tuple_cost))
        """
        if not table.has_index:
            return float("inf")
        
        btree_depth = 3.0
        matching_rows = table.total_rows * selectivity
        # Assuming unclustered random I/O: 1 page read per matching row (capped at total pages)
        random_pages = min(matching_rows, table.total_pages)
        disk_cost = (btree_depth * self.random_page_cost) + (random_pages * self.random_page_cost)
        cpu_cost = matching_rows * (self.cpu_tuple_cost + self.cpu_operator_cost)
        return round(disk_cost + cpu_cost, 2)

    def choose_scan(self, table: TableStats, selectivity: float) -> Tuple[str, float]:
        """Chooses the lowest cost scan strategy."""
        seq_cost = self.cost_seq_scan(table)
        idx_cost = self.cost_index_scan(table, selectivity)
        if idx_cost < seq_cost:
            return "Index Scan", idx_cost
        return "Sequential Scan", seq_cost

    def choose_join(
        self, 
        outer: TableStats, 
        inner: TableStats, 
        inner_has_join_index: bool = False
    ) -> Tuple[str, float]:
        """
        Compares Nested Loop vs Hash Join.
        Nested Loop: outer_rows * cost_of_inner_lookup
        Hash Join: build_hash(inner) + probe(outer)
        """
        # Nested loop with index on inner table
        if inner_has_join_index:
            nl_cost = outer.total_rows * (self.random_page_cost * 2 + self.cpu_tuple_cost)
        else:
            # Unindexed nested loop: Cartesian scan cost
            nl_cost = outer.total_rows * self.cost_seq_scan(inner)

        # Hash join: scan inner + hash build + scan outer + probe
        inner_scan = self.cost_seq_scan(inner)
        outer_scan = self.cost_seq_scan(outer)
        hash_build = inner.total_rows * (self.cpu_operator_cost * 2)
        hash_probe = outer.total_rows * self.cpu_operator_cost
        hash_cost = inner_scan + outer_scan + hash_build + hash_probe

        if nl_cost < hash_cost:
            return "Nested Loop Join", round(nl_cost, 2)
        return "Hash Join", round(hash_cost, 2)
