#!/usr/bin/env python3
"""
Execution harness for Phase 07: GROUP BY Execution Deeply
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 07: GROUP BY Execution Deeply")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT user_id, COUNT(*) FROM fact_order_items GROUP BY user_id HAVING COUNT(*) > 5;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
