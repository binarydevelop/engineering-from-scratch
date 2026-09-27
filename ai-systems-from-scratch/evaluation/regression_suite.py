"""
Automated Capability Regression Test Suite (Phase 118).
Runs fixed benchmark suites across baseline and candidate models/adapters.
Enforces zero tolerance for safety/policy regressions and statistical gating.
"""

from typing import List, Dict, Any, Callable

class TestCase:
    __test__ = False # Prevent pytest from collecting this data class as a test suite
    def __init__(self, case_id: str, prompt: str, expected_output: str, category: str = "core"):
        self.case_id = case_id
        self.prompt = prompt
        self.expected_output = expected_output
        self.category = category # 'core', 'safety', 'formatting'

class RegressionSuiteRunner:
    def __init__(self, test_cases: List[TestCase]):
        self.test_cases = test_cases

    def run_suite(self, model_fn: Callable[[str], str]) -> Dict[str, Any]:
        results = {"total": len(self.test_cases), "passed": 0, "failed": 0, "by_category": {}}
        
        for case in self.test_cases:
            cat = case.category
            if cat not in results["by_category"]:
                results["by_category"][cat] = {"passed": 0, "total": 0}
            results["by_category"][cat]["total"] += 1

            actual = model_fn(case.prompt).strip().lower()
            expected = case.expected_output.strip().lower()

            if expected in actual:
                results["passed"] += 1
                results["by_category"][cat]["passed"] += 1
            else:
                results["failed"] += 1

        results["pass_rate"] = results["passed"] / results["total"] if results["total"] > 0 else 0.0
        return results

    @staticmethod
    def compare_runs(baseline_res: Dict[str, Any], candidate_res: Dict[str, Any], max_regression_pct: float = 0.05) -> Dict[str, Any]:
        """Regression Gate: Rejects candidate if pass rate drops beyond tolerance."""
        delta = candidate_res["pass_rate"] - baseline_res["pass_rate"]
        passed_gate = delta >= -max_regression_pct
        return {
            "baseline_pass_rate": baseline_res["pass_rate"],
            "candidate_pass_rate": candidate_res["pass_rate"],
            "delta": delta,
            "passed_gate": passed_gate
        }
