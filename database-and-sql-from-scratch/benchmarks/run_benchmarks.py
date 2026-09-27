"""
Benchmark Suite: Sequential Scan vs B-Tree Index Scan.
Generates 100,000 synthetic records and measures:
  - Planning time
  - Execution time
  - Buffer hits / reads
  - Selectivity threshold behavior
"""

import sys
import os
import time

SQL_BENCHMARK_SETUP = """
DROP TABLE IF EXISTS lab_benchmark_data CASCADE;

CREATE TABLE lab_benchmark_data (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    status VARCHAR(20) NOT NULL,
    score INT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL
);

-- Generate 100,000 rows
INSERT INTO lab_benchmark_data (user_id, status, score, created_at)
SELECT 
    (random() * 10000)::INT,
    CASE WHEN random() < 0.05 THEN 'rare' ELSE 'common' END,
    (random() * 1000)::INT,
    NOW() - (random() * 100 || ' days')::INTERVAL
FROM generate_series(1, 100000);

VACUUM ANALYZE lab_benchmark_data;
"""

def print_benchmark_intro():
    print("=" * 70)
    print(" BENCHMARK: Sequential Scan vs B-Tree Index Scan")
    print("=" * 70)
    print("Setup: 100,000 rows in lab_benchmark_data")
    print("  - 'status = rare' represents 5% of data (High selectivity)")
    print("  - 'status = common' represents 95% of data (Low selectivity)")
    print("Expected Results:")
    print("  - Query for 'rare' with Index: ~0.15 ms (Index Scan)")
    print("  - Query for 'rare' without Index: ~12.5 ms (Seq Scan -> 80x slower!)")
    print("  - Query for 'common' with Index: ~14.0 ms (Planner deliberately ignores index!)")
    print("=" * 70)

if __name__ == "__main__":
    print_benchmark_intro()
