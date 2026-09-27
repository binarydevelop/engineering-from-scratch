"""
Slice-Based Evaluation Engine (Phase 119).
Prevents overall aggregate metrics from obscuring critical subset failures.
Partitions evaluations by:
- Input prompt length (short vs long context)
- Domain complexity
- Error type / Tool call presence
"""

from typing import List, Dict, Any, Callable

class SliceEvaluator:
    @staticmethod
    def evaluate_slices(records: List[Dict[str, Any]], eval_fn: Callable[[Dict[str, Any]], bool]) -> Dict[str, Dict[str, float]]:
        """
        records: list of dicts with keys: 'prompt', 'length_category', 'domain', etc.
        eval_fn: returns True if record passed, False otherwise.
        """
        slices: Dict[str, Dict[str, List[bool]]] = {
            "length": {"short": [], "medium": [], "long": []},
            "domain": {},
        }

        for r in records:
            passed = eval_fn(r)
            prompt = r.get("prompt", "")
            domain = r.get("domain", "general")

            # Length slice
            length = len(prompt.split())
            if length < 50:
                slices["length"]["short"].append(passed)
            elif length < 500:
                slices["length"]["medium"].append(passed)
            else:
                slices["length"]["long"].append(passed)

            # Domain slice
            if domain not in slices["domain"]:
                slices["domain"][domain] = []
            slices["domain"][domain].append(passed)

        # Aggregate accuracy per slice
        report: Dict[str, Dict[str, float]] = {}
        for slice_type, categories in slices.items():
            report[slice_type] = {}
            for cat, results in categories.items():
                if results:
                    report[slice_type][cat] = sum(results) / len(results)
                else:
                    report[slice_type][cat] = 0.0

        return report
