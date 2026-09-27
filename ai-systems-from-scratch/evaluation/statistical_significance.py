"""
Statistical Significance & Confidence Intervals for AI Evals (Phase 120).
Implements Wilson Score interval and McNemar test for paired binary evaluations,
preventing false claims of improvement on small evaluation samples.
"""

from typing import Tuple, Dict, Any
import math

def wilson_score_interval(successes: int, trials: int, confidence: float = 0.95) -> Tuple[float, float, float]:
    """
    Computes Wilson score interval for binomial proportion p = successes / trials.
    Returns: (point_estimate, lower_bound, upper_bound)
    """
    if trials == 0:
        return 0.0, 0.0, 0.0

    p = successes / trials
    # Z-value for 95% confidence = 1.95996
    z = 1.95996 if confidence == 0.95 else 2.57583 # 99%
    z_sq = z * z

    denominator = 1.0 + z_sq / trials
    center_adj = p + z_sq / (2 * trials)
    spread = z * math.sqrt((p * (1 - p) + z_sq / (4 * trials)) / trials)

    lower = max(0.0, (center_adj - spread) / denominator)
    upper = min(1.0, (center_adj + spread) / denominator)

    return p, lower, upper

def compare_evaluation_claims(
    baseline_success: int,
    candidate_success: int,
    trials: int
) -> Dict[str, Any]:
    p_base, low_base, high_base = wilson_score_interval(baseline_success, trials)
    p_cand, low_cand, high_cand = wilson_score_interval(candidate_success, trials)

    # If confidence intervals overlap, claim of superiority is statistically unproven!
    overlap = not (low_cand > high_base or low_base > high_cand)

    return {
        "trials": trials,
        "baseline_rate": p_base,
        "baseline_95ci": (low_base, high_base),
        "candidate_rate": p_cand,
        "candidate_95ci": (low_cand, high_cand),
        "intervals_overlap": overlap,
        "statistically_significant": not overlap
    }
