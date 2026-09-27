#!/usr/bin/env python3
"""
Execution harness for Phase 10: High-Cardinality DISTINCT Workloads
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 10: High-Cardinality DISTINCT Workloads")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT page_url, COUNT(DISTINCT user_id) FROM web_events GROUP BY page_url;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
