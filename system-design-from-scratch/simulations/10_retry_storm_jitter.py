import random
import time
from typing import List

class RetrySimulator:
    @staticmethod
    def calculate_backoff(attempt: int, base_sec: float = 0.1, cap_sec: float = 2.0, with_jitter: bool = True) -> float:
        # Full jitter formula: sleep = random(0, min(cap, base * 2^attempt))
        exponential = min(cap_sec, base_sec * (2 ** attempt))
        if with_jitter:
            return random.uniform(0, exponential)
        return exponential
