#!/usr/bin/env python3
"""
Execution harness for Phase 04: Grain: The Foundation of Analytical Correctness
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 04: Grain: The Foundation of Analytical Correctness")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT order_id, COUNT(*) AS items, SUM(net_revenue) AS order_total FROM fact_order_items GROUP BY order_id;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
