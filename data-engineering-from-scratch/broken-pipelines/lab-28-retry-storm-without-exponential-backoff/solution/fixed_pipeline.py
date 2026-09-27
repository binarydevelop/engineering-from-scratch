"""
Resilient, production-ready solution for lab-28-retry-storm-without-exponential-backoff.
"""
import random
def calculate_retry_delay_backoff(attempt, base_sec=1.0, max_sec=30.0):
    delay = min(max_sec, base_sec * (2 ** attempt))
    jitter = random.uniform(0, 0.5 * delay)
    return delay + jitter
