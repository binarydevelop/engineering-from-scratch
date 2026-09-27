"""
Broken implementation demonstrating the flaw in lab-23-stream-consumer-lag-backpressure-overflow.
"""
def estimate_backpressure_broken(prod_rate, cons_rate):
    return False # Ignores lag
