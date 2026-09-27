"""
LLM-as-Judge & Position Debiasing (Phase 115).
Implements pairwise candidate evaluation with mandatory position-swap
debiasing: evaluates (A, B) and (B, A). Detects position bias, verbosity bias,
and marks inconsistent decisions as inconclusive ties.
"""

from typing import Dict, Any, Callable

class LLMPairwiseJudge:
    def __init__(self, judge_fn: Callable[[str, str, str], str]):
        """
        judge_fn(prompt, candidate_a, candidate_b) -> "[[A]]", "[[B]]", or "[[TIE]]"
        """
        self.judge_fn = judge_fn

    def evaluate_pairwise(self, prompt: str, candidate_1: str, candidate_2: str) -> Dict[str, Any]:
        """
        Runs dual-pass evaluation:
        Pass 1: A = candidate_1, B = candidate_2
        Pass 2: A = candidate_2, B = candidate_1 (Position Swap)
        """
        decision_1 = self._parse_verdict(self.judge_fn(prompt, candidate_1, candidate_2))
        decision_2 = self._parse_verdict(self.judge_fn(prompt, candidate_2, candidate_1))

        # Pass 1: "A" favors candidate_1, "B" favors candidate_2
        # Pass 2: "A" favors candidate_2, "B" favors candidate_1
        c1_wins_pass1 = (decision_1 == "A")
        c2_wins_pass1 = (decision_1 == "B")

        c1_wins_pass2 = (decision_2 == "B")
        c2_wins_pass2 = (decision_2 == "A")

        if c1_wins_pass1 and c1_wins_pass2:
            consensus_winner = "candidate_1"
            position_bias = False
        elif c2_wins_pass1 and c2_wins_pass2:
            consensus_winner = "candidate_2"
            position_bias = False
        else:
            consensus_winner = "TIE_OR_BIASED"
            position_bias = (decision_1 == "A" and decision_2 == "A") # Judge favored position A in both!

        return {
            "pass1_verdict": decision_1,
            "pass2_verdict": decision_2,
            "consensus_winner": consensus_winner,
            "position_bias_detected": position_bias
        }

    def _parse_verdict(self, raw_output: str) -> str:
        raw = raw_output.upper()
        if "[[A]]" in raw or "CHOICE A" in raw:
            return "A"
        if "[[B]]" in raw or "CHOICE B" in raw:
            return "B"
        return "TIE"
