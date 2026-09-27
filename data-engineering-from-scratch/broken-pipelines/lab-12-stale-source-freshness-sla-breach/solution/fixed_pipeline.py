"""
Resilient, production-ready solution for lab-12-stale-source-freshness-sla-breach.
"""
def check_freshness(latest_ts, current_ts, max_lag_seconds=3600):
    lag = current_ts - latest_ts
    if lag > max_lag_seconds:
        return False, f"FRESHNESS_BREACH: Lag of {lag}s exceeds SLA of {max_lag_seconds}s"
    return True, "FRESH"
