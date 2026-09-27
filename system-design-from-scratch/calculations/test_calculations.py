"""
Pytest test suite validating all 105 back-of-the-envelope estimation exercises.
"""

import sys
import os

CALC_DIR = os.path.dirname(os.path.abspath(__file__))
if CALC_DIR not in sys.path:
    sys.path.insert(0, CALC_DIR)

from solutions import EstimationSolutions

def test_all_105_drills_computed():
    solutions = EstimationSolutions.solve_all()
    assert len(solutions) == 105, f"Expected 105 solutions, got {len(solutions)}"
    for i in range(1, 106):
        assert i in solutions, f"Missing solution for drill {i}"

def test_category_1_traffic_sample():
    solutions = EstimationSolutions.solve_all()
    # Drill 1: 10M DAU * 20 / 86400 ~ 2314.81
    assert abs(solutions[1] - 2314.81) < 1.0
    # Drill 11: 100k auctions * 5 = 500k
    assert solutions[11] == 500000

def test_category_4_cache_sample():
    solutions = EstimationSolutions.solve_all()
    # Drill 46: 500 GB * 0.20 = 100 GB
    assert solutions[46]["gb_ram"] == 100.0
    # Drill 53: 10,000 * 0.05 = 500 QPS
    assert solutions[53]["db_qps"] == 500

def test_category_5_littles_law_sample():
    solutions = EstimationSolutions.solve_all()
    # Drill 61: 2500 * 0.080 = 200
    assert solutions[61]["concurrency"] == 200
    # Drill 63: 200 * 0.500 = 100
    assert solutions[63]["connections"] == 100

def test_category_7_availability_sample():
    solutions = EstimationSolutions.solve_all()
    # Drill 87: 99.99% downtime per year is ~52.56 minutes
    assert abs(solutions[87]["minutes_downtime"] - 52.56) < 0.1
    # Drill 95: SLA violated
    assert solutions[95]["violated"] is True
