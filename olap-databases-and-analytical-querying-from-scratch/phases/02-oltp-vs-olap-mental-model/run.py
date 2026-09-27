#!/usr/bin/env python3
"""
Execution harness for Phase 02: OLTP vs OLAP Architecture
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 02: OLTP vs OLAP Architecture")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''EXPLAIN ANALYZE SELECT country, SUM(net_revenue) FROM fact_order_items GROUP BY country;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
