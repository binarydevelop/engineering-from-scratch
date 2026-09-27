"""
Benchmark: Keyset/Cursor Pagination vs Deep OFFSET Pagination.
Demonstrates why OFFSET pagination degrades linearly O(N) as pages get deep,
while Keyset (WHERE id > cursor) pagination remains O(1) indexed constant time.
"""

import time
import sqlite3
from typing import Dict, Any

def setup_db(conn: sqlite3.Connection, num_rows: int = 25000):
    conn.execute("CREATE TABLE records (id INTEGER PRIMARY KEY, title TEXT, score REAL)")
    rows = [(i, f"Title {i}", i * 1.5) for i in range(1, num_rows + 1)]
    conn.executemany("INSERT INTO records VALUES (?, ?, ?)", rows)
    conn.commit()

def benchmark() -> Dict[str, Any]:
    conn = sqlite3.connect(":memory:")
    setup_db(conn, 25000)

    # 1. Deep OFFSET pagination (scans and discards 20,000 rows)
    start_offset = time.perf_counter()
    cur = conn.cursor()
    for _ in range(50):
        cur.execute("SELECT id, title FROM records ORDER BY id LIMIT 20 OFFSET 20000")
        cur.fetchall()
    offset_time = time.perf_counter() - start_offset

    # 2. Keyset/Cursor pagination (uses B-Tree index seek directly to id 20000)
    start_cursor = time.perf_counter()
    for _ in range(50):
        cur.execute("SELECT id, title FROM records WHERE id > 20000 ORDER BY id LIMIT 20")
        cur.fetchall()
    cursor_time = time.perf_counter() - start_cursor

    conn.close()
    speedup = offset_time / cursor_time if cursor_time > 0 else 1.0

    return {
        "name": "Cursor/Keyset vs Deep OFFSET Pagination",
        "offset_time_sec": round(offset_time, 4),
        "cursor_time_sec": round(cursor_time, 4),
        "speedup_ratio": round(speedup, 2)
    }

if __name__ == "__main__":
    res = benchmark()
    print(f"[{res['name']}]")
    print(f"  OFFSET 20000: {res['offset_time_sec']}s")
    print(f"  Keyset Seek:  {res['cursor_time_sec']}s")
    print(f"  Speedup:      {res['speedup_ratio']}x")
