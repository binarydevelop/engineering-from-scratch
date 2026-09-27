"""
Benchmark: Fresh Connection Per Request vs Connection Pooling / Connection Reuse.
Measures the latency overhead of TCP/socket/file-descriptor handshakes per query.
"""

import time
import sqlite3
import tempfile
import os
from typing import Dict, Any

def run_without_pooling(db_path: str, iterations: int = 200) -> float:
    start = time.perf_counter()
    for _ in range(iterations):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.fetchone()
        conn.close()
    return time.perf_counter() - start

def run_with_pooling(db_path: str, iterations: int = 200) -> float:
    start = time.perf_counter()
    # Reusing a persistent/pooled connection
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for _ in range(iterations):
        cur.execute("SELECT 1")
        cur.fetchone()
    conn.close()
    return time.perf_counter() - start

def benchmark() -> Dict[str, Any]:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        tmp_db = f.name

    try:
        iterations = 250
        time_no_pool = run_without_pooling(tmp_db, iterations)
        time_pool = run_with_pooling(tmp_db, iterations)
        speedup = time_no_pool / time_pool if time_pool > 0 else 1.0

        return {
            "name": "Connection Overhead vs Connection Reuse",
            "queries": iterations,
            "without_pool_sec": round(time_no_pool, 4),
            "with_pool_sec": round(time_pool, 4),
            "speedup_ratio": round(speedup, 2)
        }
    finally:
        if os.path.exists(tmp_db):
            os.remove(tmp_db)

if __name__ == "__main__":
    res = benchmark()
    print(f"[{res['name']}]")
    print(f"  Without Pool: {res['without_pool_sec']}s")
    print(f"  With Pool:    {res['with_pool_sec']}s")
    print(f"  Speedup:      {res['speedup_ratio']}x")
