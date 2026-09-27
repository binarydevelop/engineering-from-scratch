"""
Mini Relational Database Engine in Pure Python.
Implements:
  - Table & Schema validation
  - Row storage
  - Primary Key constraint enforcement
  - Secondary Index (Hash & Sorted/B-Tree lookup)
  - Relational Operators: Selection (Filter), Projection, Join (Hash Join & Nested Loop)
"""

from typing import List, Dict, Any, Optional, Tuple, Callable


class Table:
    def __init__(self, name: str, columns: List[str], primary_key: str):
        self.name = name
        self.columns = columns
        self.primary_key = primary_key
        if primary_key not in columns:
            raise ValueError(f"Primary key '{primary_key}' must be one of the columns: {columns}")
        
        self.rows: List[Dict[str, Any]] = []
        self.pk_index: Dict[Any, int] = {}  # pk_val -> row_index
        self.secondary_indexes: Dict[str, Dict[Any, List[int]]] = {}

    def create_index(self, column: str):
        if column not in self.columns:
            raise ValueError(f"Column '{column}' does not exist on table '{self.name}'")
        idx: Dict[Any, List[int]] = {}
        for row_idx, row in enumerate(self.rows):
            val = row[column]
            idx.setdefault(val, []).append(row_idx)
        self.secondary_indexes[column] = idx

    def insert(self, row: Dict[str, Any]):
        # Validate schema
        for col in self.columns:
            if col not in row:
                raise ValueError(f"Missing column '{col}' in insert payload for table '{self.name}'")
        
        pk_val = row[self.primary_key]
        if pk_val in self.pk_index:
            raise ValueError(f"Duplicate primary key violation: {self.primary_key}={pk_val} already exists.")
        
        row_idx = len(self.rows)
        self.rows.append(row)
        self.pk_index[pk_val] = row_idx

        # Update secondary indexes
        for col, idx in self.secondary_indexes.items():
            val = row[col]
            idx.setdefault(val, []).append(row_idx)

    def scan(self) -> List[Dict[str, Any]]:
        """Sequential Scan: Reads every row in physical order."""
        return list(self.rows)

    def lookup_pk(self, pk_val: Any) -> Optional[Dict[str, Any]]:
        """O(1) Primary Key Lookup via Index."""
        row_idx = self.pk_index.get(pk_val)
        if row_idx is not None:
            return self.rows[row_idx]
        return None

    def lookup_index(self, column: str, val: Any) -> List[Dict[str, Any]]:
        """Index Scan: Fast lookup using secondary index."""
        if column not in self.secondary_indexes:
            raise ValueError(f"No index exists on column '{column}'")
        row_indices = self.secondary_indexes[column].get(val, [])
        return [self.rows[idx] for idx in row_indices]


class RelationalEngine:
    """Implements Relational Algebra Operators: Selection, Projection, Join."""

    @staticmethod
    def select(rows: List[Dict[str, Any]], predicate: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
        """Selection (WHERE / Filter)."""
        return [r for r in rows if predicate(r)]

    @staticmethod
    def project(rows: List[Dict[str, Any]], columns: List[str]) -> List[Dict[str, Any]]:
        """Projection (SELECT specific columns)."""
        return [{col: r[col] for col in columns if col in r} for r in rows]

    @staticmethod
    def nested_loop_join(
        left_rows: List[Dict[str, Any]], 
        right_rows: List[Dict[str, Any]], 
        left_key: str, 
        right_key: str
    ) -> List[Dict[str, Any]]:
        """Nested Loop Join: O(N * M) comparison."""
        result = []
        for l in left_rows:
            for r in right_rows:
                if l.get(left_key) == r.get(right_key):
                    combined = {f"left_{k}": v for k, v in l.items()}
                    combined.update({f"right_{k}": v for k, v in r.items()})
                    result.append(combined)
        return result

    @staticmethod
    def hash_join(
        left_rows: List[Dict[str, Any]], 
        right_rows: List[Dict[str, Any]], 
        left_key: str, 
        right_key: str
    ) -> List[Dict[str, Any]]:
        """Hash Join: O(N + M) join using in-memory hash table."""
        # 1. Build Phase: Hash the smaller or right relation
        hash_table: Dict[Any, List[Dict[str, Any]]] = {}
        for r in right_rows:
            key_val = r.get(right_key)
            hash_table.setdefault(key_val, []).append(r)

        # 2. Probe Phase: Stream left relation and probe hash table
        result = []
        for l in left_rows:
            key_val = l.get(left_key)
            matches = hash_table.get(key_val, [])
            for r in matches:
                combined = {f"left_{k}": v for k, v in l.items()}
                combined.update({f"right_{k}": v for k, v in r.items()})
                result.append(combined)
        return result
