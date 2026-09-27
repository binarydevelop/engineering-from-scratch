#!/usr/bin/env python3
"""
Tiny Column Store: An Educational OLAP Engine from Scratch.
Implements:
  - Separate binary files per column (.col)
  - Dictionary encoding for categorical strings
  - Block-level zone maps (min/max metadata per 1024 rows)
  - Projection pushdown (reading only requested column files)
  - Predicate pushdown via zone-map block skipping
  - Vectorized aggregation (SUM, COUNT, GROUP BY)
"""

import os
import struct
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional

BLOCK_SIZE = 1024

class TinyColumnStore:
    def __init__(self, table_dir: Path):
        self.table_dir = Path(table_dir)
        self.table_dir.mkdir(parents=True, exist_ok=True)
        self.meta_file = self.table_dir / "metadata.json"
        self.metadata = {
            "num_rows": 0,
            "columns": {}, # name: {"type": "int64"|"float64"|"string_dict", "num_blocks": 0}
            "blocks": []   # [{"block_id": 0, "num_rows": 1024, "stats": {col: {"min": x, "max": y}}}]
        }
        if self.meta_file.exists():
            with open(self.meta_file, "r") as f:
                self.metadata = json.load(f)

    def write_table(self, data: Dict[str, list]):
        """
        Writes in-memory column data into columnar on-disk files.
        Supported types:
          - int: 64-bit signed int ('<q')
          - float: 64-bit float ('<d')
          - str: dictionary encoded ('<H')
        """
        num_rows = len(next(iter(data.values())))
        self.metadata["num_rows"] = num_rows
        
        # 1. Inspect schemas and prepare column files
        col_handlers = {}
        for col_name, values in data.items():
            first_val = values[0]
            if isinstance(first_val, int):
                col_handlers[col_name] = {"type": "int64", "pack_char": "<q"}
            elif isinstance(first_val, float):
                col_handlers[col_name] = {"type": "float64", "pack_char": "<d"}
            elif isinstance(first_val, str):
                unique_strings = sorted(list(set(values)))
                str_to_id = {s: i for i, s in enumerate(unique_strings)}
                col_handlers[col_name] = {
                    "type": "string_dict",
                    "dictionary": unique_strings,
                    "str_to_id": str_to_id,
                    "pack_char": "<H" # up to 65535 unique strings
                }
            self.metadata["columns"][col_name] = {
                "type": col_handlers[col_name]["type"],
                "dictionary": col_handlers[col_name].get("dictionary")
            }

        # 2. Write blocks and compute Zone Maps
        self.metadata["blocks"] = []
        num_blocks = (num_rows + BLOCK_SIZE - 1) // BLOCK_SIZE
        
        # Open file descriptors for each column
        fds = {col: open(self.table_dir / f"{col}.col", "wb") for col in data}
        
        for b in range(num_blocks):
            start_idx = b * BLOCK_SIZE
            end_idx = min(start_idx + BLOCK_SIZE, num_rows)
            b_rows = end_idx - start_idx
            
            block_meta = {
                "block_id": b,
                "num_rows": b_rows,
                "stats": {}
            }
            
            for col_name, values in data.items():
                handler = col_handlers[col_name]
                slice_vals = values[start_idx:end_idx]
                
                if handler["type"] == "string_dict":
                    id_vals = [handler["str_to_id"][s] for s in slice_vals]
                    # Pack as 16-bit unsigned ints
                    packed = struct.pack(f"<{len(id_vals)}H", *id_vals)
                    block_meta["stats"][col_name] = {
                        "min": min(slice_vals),
                        "max": max(slice_vals),
                        "min_id": min(id_vals),
                        "max_id": max(id_vals)
                    }
                else:
                    packed = struct.pack(f"{handler['pack_char'][0]}{len(slice_vals)}{handler['pack_char'][1]}", *slice_vals)
                    block_meta["stats"][col_name] = {
                        "min": min(slice_vals),
                        "max": max(slice_vals)
                    }
                fds[col_name].write(packed)
                
            self.metadata["blocks"].append(block_meta)
            
        for fd in fds.values():
            fd.close()
            
        with open(self.meta_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def query(self,
              select_cols: List[str],
              where_col: Optional[str] = None,
              where_op: Optional[str] = None,
              where_val: Optional[Any] = None,
              group_by_col: Optional[str] = None,
              agg_col: Optional[str] = None) -> Tuple[Dict[str, Any], int, int]:
        """
        Executes analytical query using:
          - Projection pushdown (reading only select_cols, where_col, group_by_col, agg_col)
          - Zone-map data skipping (bypassing entire blocks)
        """
        needed_cols = set(select_cols)
        if where_col: needed_cols.add(where_col)
        if group_by_col: needed_cols.add(group_by_col)
        if agg_col: needed_cols.add(agg_col)
        
        blocks_scanned = 0
        blocks_skipped = 0
        
        # Load dictionaries for needed string cols
        dicts = {}
        for col in needed_cols:
            if self.metadata["columns"][col]["type"] == "string_dict":
                dicts[col] = self.metadata["columns"][col]["dictionary"]

        results_agg = {} # group_val -> [count, sum]
        
        # Open only needed column files!
        fds = {col: open(self.table_dir / f"{col}.col", "rb") for col in needed_cols}
        
        for b_meta in self.metadata["blocks"]:
            b_id = b_meta["block_id"]
            b_rows = b_meta["num_rows"]
            
            # --- 1. Zone Map Skipping Check ---
            skip_block = False
            if where_col and where_op and where_col in b_meta["stats"]:
                col_stats = b_meta["stats"][where_col]
                c_min, c_max = col_stats["min"], col_stats["max"]
                if where_op == ">" and c_max <= where_val:
                    skip_block = True
                elif where_op == ">=" and c_max < where_val:
                    skip_block = True
                elif where_op == "<" and c_min >= where_val:
                    skip_block = True
                elif where_op == "<=" and c_min > where_val:
                    skip_block = True
                elif where_op == "==" and (where_val < c_min or where_val > c_max):
                    skip_block = True
                    
            if skip_block:
                blocks_skipped += 1
                # Fast forward file pointers!
                for col in needed_cols:
                    pack_size = 2 if self.metadata["columns"][col]["type"] == "string_dict" else 8
                    fds[col].seek(pack_size * b_rows, os.SEEK_CUR)
                continue
                
            blocks_scanned += 1
            
            # --- 2. Read Column Vectors ---
            loaded_vectors = {}
            for col in needed_cols:
                col_type = self.metadata["columns"][col]["type"]
                if col_type == "string_dict":
                    raw = fds[col].read(2 * b_rows)
                    id_vals = struct.unpack(f"<{b_rows}H", raw)
                    d = dicts[col]
                    loaded_vectors[col] = [d[idx] for idx in id_vals]
                elif col_type == "int64":
                    raw = fds[col].read(8 * b_rows)
                    loaded_vectors[col] = struct.unpack(f"<{b_rows}q", raw)
                elif col_type == "float64":
                    raw = fds[col].read(8 * b_rows)
                    loaded_vectors[col] = struct.unpack(f"<{b_rows}d", raw)

            # --- 3. Filter and Aggregate ---
            for i in range(b_rows):
                # Filter
                if where_col:
                    val = loaded_vectors[where_col][i]
                    if where_op == ">" and not (val > where_val): continue
                    if where_op == ">=" and not (val >= where_val): continue
                    if where_op == "<" and not (val < where_val): continue
                    if where_op == "<=" and not (val <= where_val): continue
                    if where_op == "==" and not (val == where_val): continue
                    
                grp = loaded_vectors[group_by_col][i] if group_by_col else "ALL"
                m_val = loaded_vectors[agg_col][i] if agg_col else 1
                
                if grp not in results_agg:
                    results_agg[grp] = [0, 0.0]
                results_agg[grp][0] += 1
                results_agg[grp][1] += float(m_val)
                
        for fd in fds.values():
            fd.close()
            
        return results_agg, blocks_scanned, blocks_skipped

if __name__ == "__main__":
    import random
    table_path = Path("outputs/tiny_col_store")
    db = TinyColumnStore(table_path)
    
    # Generate 50,000 synthetic rows
    n = 50_000
    print(f"[*] Generating {n:,} rows for TinyColumnStore...")
    countries = ["US", "DE", "UK", "JP", "FR", "IN"]
    categories = ["Electronics", "Apparel", "Home", "Books"]
    
    # Data sorted by created_at to empower zone maps
    data = {
        "created_at": [1700000000 + (i * 10) for i in range(n)],
        "country": [countries[i % len(countries)] for i in range(n)],
        "category": [categories[(i // 1000) % len(categories)] for i in range(n)],
        "revenue": [round(15.0 + (i % 200) * 1.5, 2) for i in range(n)],
        "quantity": [(i % 5) + 1 for i in range(n)]
    }
    
    print("[*] Writing columnar files and computing Zone Maps...")
    db.write_table(data)
    print(f"  [✓] Table written to {table_path} with {len(db.metadata['blocks'])} blocks.")
    
    # Run query with Zone Map pruning on created_at
    # Query: created_at >= 1700400000 (only last 20% of data)
    cutoff = 1700000000 + int(n * 10 * 0.8)
    print(f"\n[*] Query: SELECT country, SUM(revenue) WHERE created_at >= {cutoff} GROUP BY country")
    agg_res, scanned, skipped = db.query(
        select_cols=["country", "revenue"],
        where_col="created_at",
        where_op=">=",
        where_val=cutoff,
        group_by_col="country",
        agg_col="revenue"
    )
    
    print(f"  Blocks Scanned: {scanned} / {len(db.metadata['blocks'])}")
    print(f"  Blocks Skipped: {skipped} ({(skipped / len(db.metadata['blocks'])) * 100:.1f}%)")
    print(f"  Aggregated Results:")
    for country, (cnt, total_rev) in agg_res.items():
        print(f"    - {country}: {cnt:,} items, ${total_rev:,.2f} revenue")
