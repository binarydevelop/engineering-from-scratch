"""
Resilient, production-ready solution for lab-23-stream-consumer-lag-backpressure-overflow.
"""
def estimate_lag_growth(prod_rate, cons_rate, elapsed_sec):
    deficit = prod_rate - cons_rate
    return max(0, deficit * elapsed_sec)
