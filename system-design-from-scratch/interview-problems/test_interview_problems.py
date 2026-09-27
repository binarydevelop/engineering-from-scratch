"""
Pytest test suite validating completeness and structure of all 50 System Design Interview Problems.
"""

import os
import glob
import pytest

PROBLEMS_DIR = os.path.dirname(os.path.abspath(__file__))

def test_problem_counts_by_tier():
    beginner = glob.glob(os.path.join(PROBLEMS_DIR, "beginner", "prob-*"))
    intermediate = glob.glob(os.path.join(PROBLEMS_DIR, "intermediate", "prob-*"))
    advanced = glob.glob(os.path.join(PROBLEMS_DIR, "advanced", "prob-*"))

    assert len(beginner) == 15, f"Expected 15 beginner problems, found {len(beginner)}"
    assert len(intermediate) == 20, f"Expected 20 intermediate problems, found {len(intermediate)}"
    assert len(advanced) == 15, f"Expected 15 advanced problems, found {len(advanced)}"
    assert (len(beginner) + len(intermediate) + len(advanced)) == 50

def test_every_problem_has_problem_and_solution_files():
    all_dirs = glob.glob(os.path.join(PROBLEMS_DIR, "*", "prob-*"))
    assert len(all_dirs) == 50

    for p_dir in all_dirs:
        prob_file = os.path.join(p_dir, "problem.md")
        sol_file = os.path.join(p_dir, "solution.md")

        assert os.path.isfile(prob_file), f"Missing problem.md in {p_dir}"
        assert os.path.isfile(sol_file), f"Missing solution.md in {p_dir}"

        with open(prob_file, "r", encoding="utf-8") as f:
            p_text = f.read()
            assert "Requirements" in p_text
            assert "Scale Estimations" in p_text
            assert "Failure Scenarios" in p_text

        with open(sol_file, "r", encoding="utf-8") as f:
            s_text = f.read()
            assert "Architectural Solution" in s_text
            assert "Component Architecture" in s_text
            assert "Tradeoffs" in s_text
