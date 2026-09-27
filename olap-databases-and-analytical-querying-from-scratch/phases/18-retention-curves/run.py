#!/usr/bin/env python3
"""
Execution harness for Phase 18: N-Day Activity Retention Curves
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 18: N-Day Activity Retention Curves")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT u.user_id, min(date_trunc('day', e.event_time)) as first_day FROM web_events e JOIN dim_users u ON e.user_id = u.user_id GROUP BY 1;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
