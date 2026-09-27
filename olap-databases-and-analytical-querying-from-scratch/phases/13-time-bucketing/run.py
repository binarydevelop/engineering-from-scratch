#!/usr/bin/env python3
"""
Execution harness for Phase 13: Temporal Bucketing and Continuous Resampling
"""
import duckdb
import time

def main():
    print(f"[*] Executing Phase 13: Temporal Bucketing and Continuous Resampling")
    con = duckdb.connect('outputs/olap_lab.duckdb', read_only=True)
    t0 = time.perf_counter()
    try:
        res = con.execute('''SELECT date_trunc('hour', timestamp) AS hour_bucket, AVG(temperature_c), AVG(pressure_kpa) FROM sensor_readings GROUP BY 1 ORDER BY 1;''').fetchall()
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        print(f"  [✓] Query executed successfully in {elapsed_ms:.2f} ms (Returned {len(res)} rows)")
    except Exception as e:
        print(f"  [!] Note: {e} (Table may require specific setup)")
    finally:
        con.close()

if __name__ == '__main__':
    main()
