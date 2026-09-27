#!/usr/bin/env python3
"""
Execution harness for Phase 08: Aggregations & Three-Valued NULL Semantics
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 08: Aggregations & Three-Valued NULL Semantics")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT service_name, COUNT(*), COUNT(error_code), AVG(latency_ms) FROM service_logs GROUP BY service_name;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
