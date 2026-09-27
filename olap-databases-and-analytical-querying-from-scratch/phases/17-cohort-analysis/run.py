#!/usr/bin/env python3
"""
Execution harness for Phase 17: Cohort Analysis
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 17: Cohort Analysis")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT u.signup_date, date_trunc('month', f.created_at) as order_month, COUNT(DISTINCT f.user_id) FROM fact_order_items f JOIN dim_users u ON f.user_id = u.user_id GROUP BY 1, 2;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
