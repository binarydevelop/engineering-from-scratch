#!/usr/bin/env python3
"""
Execution harness for Phase 19: Clickstream Sessionization using Time Gaps
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 19: Clickstream Sessionization using Time Gaps")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT user_id, event_time, LAG(event_time) OVER (PARTITION BY user_id ORDER BY event_time) as prev_time FROM web_events;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
