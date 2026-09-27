#!/usr/bin/env python3
"""
Execution harness for Phase 15: Top-N Ranking per Analytical Partition
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 15: Top-N Ranking per Analytical Partition")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''WITH ranked AS (SELECT country, product_id, SUM(net_revenue) as rev, DENSE_RANK() OVER (PARTITION BY country ORDER BY SUM(net_revenue) DESC) as rk FROM fact_order_items GROUP BY country, product_id) SELECT * FROM ranked WHERE rk <= 5;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
