"""
Sequence Length Distribution Analyzer (Phase 87).
Profiles token length distributions across instructional datasets,
calculating p50, p90, p95, and p99 percentiles, and determining optimal
max_seq_len to minimize truncation while preventing wasted padding.
"""

from typing import List, Dict
import numpy as np

class SequenceLengthAnalyzer:
    def __init__(self):
        pass

    def analyze_token_lengths(self, lengths: List[int]) -> Dict[str, float]:
        arr = np.array(lengths)
        return {
            "count": len(arr),
            "min": int(np.min(arr)),
            "max": int(np.max(arr)),
            "mean": float(np.mean(arr)),
            "median_p50": float(np.percentile(arr, 50)),
            "p90": float(np.percentile(arr, 90)),
            "p95": float(np.percentile(arr, 95)),
            "p99": float(np.percentile(arr, 99))
        }

    def compute_truncation_loss(self, lengths: List[int], target_cutoff: int) -> Dict[str, float]:
        arr = np.array(lengths)
        truncated_samples = int(np.sum(arr > target_cutoff))
        percent_truncated = (truncated_samples / len(arr)) * 100.0
        tokens_discarded = int(np.sum(np.maximum(0, arr - target_cutoff)))
        total_tokens = int(np.sum(arr))

        return {
            "target_cutoff": target_cutoff,
            "truncated_samples": truncated_samples,
            "percent_samples_truncated": percent_truncated,
            "tokens_discarded": tokens_discarded,
            "percent_tokens_discarded": (tokens_discarded / total_tokens) * 100.0 if total_tokens > 0 else 0.0
        }
