"""
Broken implementation demonstrating the flaw in lab-28-retry-storm-without-exponential-backoff.
"""
def calculate_retry_delay_broken(attempt):
    return 0 # Immediate retry creates storm
