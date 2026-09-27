#!/usr/bin/env python3
"""
Execution harness for Phase 16: Conversion Funnels Analysis
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 16: Conversion Funnels Analysis")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT COUNT(DISTINCT CASE WHEN event_type = 'view' THEN user_id END) as v, COUNT(DISTINCT CASE WHEN event_type = 'add_to_cart' THEN user_id END) as c, COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN user_id END) as p FROM web_events;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
