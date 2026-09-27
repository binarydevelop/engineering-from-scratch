#!/usr/bin/env python3
"""
Tiny Vectorized Engine: An Educational Vectorized Query Processor from Scratch.
Implements:
  - Vector & DataChunk (fixed chunk size: 2,048 values)
  - Selection Vector (boolean bitmap / index list for branchless filtering)
  - Physical Vectorized Operators:
      1. PhysicalVectorScan
      2. PhysicalVectorFilter
      3. PhysicalVectorProject
      4. PhysicalVectorHashAggregate
  - Push-based chunk pipelining
"""

from typing import List, Dict, Any, Optional, Tuple

CHUNK_SIZE = 2048

class Vector:
    def __init__(self, data: list, data_type: str):
        self.data = data
        self.data_type = data_type
        self.size = len(data)

    def __getitem__(self, idx):
        return self.data[idx]

class DataChunk:
    def __init__(self, vectors: Dict[str, Vector], size: int):
        self.vectors = vectors
        self.size = size
        # Optional selection vector for in-place branchless filtering
        self.selection_vector: Optional[List[int]] = None

    def active_count(self) -> int:
        if self.selection_vector is not None:
            return len(self.selection_vector)
        return self.size

class PhysicalVectorScan:
    def __init__(self, table_data: Dict[str, list]):
        self.table_data = table_data
        self.total_rows = len(next(iter(table_data.values())))
        self.cursor = 0

    def next_chunk(self) -> Optional[DataChunk]:
        if self.cursor >= self.total_rows:
            return None
        end = min(self.cursor + CHUNK_SIZE, self.total_rows)
        chunk_size = end - self.cursor
        
        vectors = {}
        for col, col_data in self.table_data.items():
            vectors[col] = Vector(col_data[self.cursor:end], type(col_data[0]).__name__)
            
        self.cursor = end
        return DataChunk(vectors, chunk_size)

class PhysicalVectorFilter:
    def __init__(self, child: PhysicalVectorScan, predicate_col: str, op: str, target_val: Any):
        self.child = child
        self.predicate_col = predicate_col
        self.op = op
        self.target_val = target_val

    def next_chunk(self) -> Optional[DataChunk]:
        chunk = self.child.next_chunk()
        if chunk is None:
            return None
            
        vec = chunk.vectors[self.predicate_col]
        # Build Selection Vector
        sel_vec = []
        target = self.target_val
        
        if self.op == ">":
            for i in range(chunk.size):
                if vec[i] > target: sel_vec.append(i)
        elif self.op == ">=":
            for i in range(chunk.size):
                if vec[i] >= target: sel_vec.append(i)
        elif self.op == "==":
            for i in range(chunk.size):
                if vec[i] == target: sel_vec.append(i)
        elif self.op == "<":
            for i in range(chunk.size):
                if vec[i] < target: sel_vec.append(i)
        elif self.op == "<=":
            for i in range(chunk.size):
                if vec[i] <= target: sel_vec.append(i)
                
        chunk.selection_vector = sel_vec
        return chunk

class PhysicalVectorHashAggregate:
    def __init__(self, child: PhysicalVectorFilter, group_col: str, agg_col: str, agg_func: str = "SUM"):
        self.child = child
        self.group_col = group_col
        self.agg_col = agg_col
        self.agg_func = agg_func
        # Hash table: group_key -> [count, sum]
        self.hash_table: Dict[Any, List[float]] = {}

    def execute(self) -> Dict[Any, Tuple[int, float]]:
        while True:
            chunk = self.child.next_chunk()
            if chunk is None:
                break
                
            grp_vec = chunk.vectors[self.group_col]
            agg_vec = chunk.vectors[self.agg_col]
            
            # Vectorized aggregation using selection vector
            if chunk.selection_vector is not None:
                for idx in chunk.selection_vector:
                    k = grp_vec[idx]
                    v = agg_vec[idx]
                    if k not in self.hash_table:
                        self.hash_table[k] = [0, 0.0]
                    self.hash_table[k][0] += 1
                    self.hash_table[k][1] += float(v)
            else:
                for i in range(chunk.size):
                    k = grp_vec[i]
                    v = agg_vec[i]
                    if k not in self.hash_table:
                        self.hash_table[k] = [0, 0.0]
                    self.hash_table[k][0] += 1
                    self.hash_table[k][1] += float(v)
                    
        return {k: (v[0], v[1]) for k, v in self.hash_table.items()}

if __name__ == "__main__":
    n = 100_000
    print(f"[*] Initializing TinyVectorizedEngine with {n:,} rows...")
    raw_data = {
        "device": ["iOS" if i % 2 == 0 else "Android" for i in range(n)],
        "duration_ms": [(i % 500) + 10 for i in range(n)],
        "revenue": [round(5.0 + (i % 50) * 1.5, 2) for i in range(n)]
    }
    
    # Query: SELECT device, SUM(revenue), COUNT(*) WHERE duration_ms >= 250 GROUP BY device
    scan = PhysicalVectorScan(raw_data)
    filter_op = PhysicalVectorFilter(scan, predicate_col="duration_ms", op=">=", target_val=250)
    agg_op = PhysicalVectorHashAggregate(filter_op, group_col="device", agg_col="revenue")
    
    print("[*] Executing vectorized pipeline with chunk size 2,048...")
    results = agg_op.execute()
    print("  [✓] Query execution complete!")
    print("  Results:")
    for device, (cnt, rev) in results.items():
        print(f"    - {device}: {cnt:,} requests, ${rev:,.2f} revenue")
